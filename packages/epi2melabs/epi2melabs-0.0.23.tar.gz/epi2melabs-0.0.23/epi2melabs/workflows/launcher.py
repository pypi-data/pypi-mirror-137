# flake8: noqa
import re
import os
import json
import signal
import shutil
import requests
import shortuuid
import subprocess
from datetime import datetime
from dataclasses import dataclass
from urllib.parse import quote_plus
from nf_core.schema import PipelineSchema
from jsonschema.validators import validator_for
from typing import Callable, Dict, Type, TypedDict, Union, Tuple, List, Any
from epi2melabs.workflows.database import Statuses, get_session, Instance


class LauncherException(Exception):
    ...


class Path(TypedDict):
    name: str
    path: str
    isdir: bool
    updated: float

class PathResponse(TypedDict):
    path: str
    exists: bool
    error: Union[str, None]

class FilePathResponse(PathResponse):
    contents: Union[None, List[str]]

class DirectoryPathResponse(PathResponse):
    contents: Union[None, List[Path]]

class InstanceCreateResponse(TypedDict):
    created: bool
    instance: dict
    error: Union[str, None]

@dataclass
class Workflow:
    url: str
    name: str
    desc: str
    path: str
    target: str
    schema: Dict
    defaults: Dict

    def to_dict(self):
        return {
            'url': self.url,
            'name': self.name,
            'desc': self.desc,
            'path': self.path,
            'target': self.target,
            'schema': self.schema,
            'defaults': self.defaults}


class WorkflowLauncher(object):
    MAINNF: str = 'main.nf'
    PARAMS: str = 'params.json'
    SCHEMA: str = 'nextflow_schema.json'
    
    def __init__(self, base_dir=None, workflows_dir=None,
        invoker='invoke_nextflow', nextflow='nextflow') -> None:

        self._workflows: Dict[str, Workflow] = {}

        self.curr_dir = os.getcwd()
        self.base_dir = base_dir or os.path.join(os.getcwd(), 'nextflow')
        self.workflows_dir = workflows_dir or os.path.join(self.base_dir, 'workflows')
        self.instance_dir = os.path.join(self.base_dir, 'instances')
        self.database_uri = f'sqlite:///{self.base_dir}/db.sqlite'

        self.invoker = invoker
        self.nextflow = nextflow

        self.get_or_create_dir(self.base_dir)
        self.get_or_create_dir(self.instance_dir)
        self.get_or_create_dir(self.workflows_dir)
        self.db = get_session(self.database_uri)

    #
    # Workflows
    #
    @property
    def workflows(self) -> Dict:
        for item in os.listdir(self.workflows_dir):
            if self._workflows.get(item):
                continue
            path = os.path.join(self.workflows_dir, item)
            if not os.path.isdir(path):
                continue
            if not self.SCHEMA in os.listdir(path):
                continue
            try:
                self._workflows[item] = self.load_workflow(
                    item, path)
            except LauncherException:
                pass
        return {
            workflow.name: workflow.to_dict()
            for workflow in self._workflows.values()
        }

    def get_workflow(self, name: str) -> Dict:
        if workflow := self.workflows.get(name):
            return workflow
        return {}

    def _get_workflow(self, name: str) -> Union[Workflow, None]:
        if not self.workflows:
            pass
        if workflow := self._workflows.get(name):
            return workflow
        return None

    def load_workflow(self, name: str, path: str) -> Workflow:
        nfcore = PipelineSchema()
        nfcore.get_schema_path(path)
        nfcore.load_schema()
        nfcore.get_schema_defaults()

        if not nfcore.schema:
            raise LauncherException(
                f'Cannot reload {name}: missing schema')

        target = None
        main_nf = os.path.join(path, self.MAINNF)
        if os.path.exists(main_nf):
            target = main_nf

        if not target:
            target = nfcore.schema.get('title')
            if ' ' in target:
                raise LauncherException(
                    'Cannot load {name}: invalid title')

        if not target:
            raise LauncherException(
                'Cannot load {name}: no entrypoint')

        return Workflow(
            name = name,
            path = path,
            target = target,
            schema = nfcore.schema,
            defaults = nfcore.schema_defaults,
            url =  nfcore.schema.get('url', '#'),
            desc = nfcore.schema.get('description', ''))

    #
    # Instances
    #
    @property
    def instances(self) -> Dict:
        return {
            instance.id: instance.to_dict()
            for instance in self.db.query(Instance).all()
        }

    def get_instance(self, id: str) -> Dict:
        if instance := self._get_instance(id):
            return instance.to_dict()
        return {}

    def _get_instance(self, id: str) -> Union[Instance, None]:
        if instance := self.db.query(Instance).get(id):
            return instance
        return None

    def create_instance(
        self, name: str, workflow_name: str, params: Dict
    ) -> InstanceCreateResponse:
        workflow = self._get_workflow(workflow_name)

        if not workflow or not workflow.target:
            return InstanceCreateResponse(
                created=False, instance={},
                error='Could not create instance, workflow unknown')

        return self._create_instance(
            name, workflow.name, workflow.target, params)

    def _create_instance(
        self, name: str, workflow_name: str, workflow_target: str, params: Dict
    ) -> InstanceCreateResponse:

        # Generate instance details
        _id = str(shortuuid.uuid())
        now = datetime.now().strftime("%Y-%m-%d-%H-%M")
        dirname = '_'.join([now, workflow_name, _id])
        path = os.path.join(self.instance_dir, dirname)

        # Create instance db record
        instance = Instance(_id, path, name, workflow_name)
        self.db.add(instance)
        self.db.commit()

        # Construct instance filepaths
        params_file = os.path.join(path, self.PARAMS)
        nf_logfile = os.path.join(path, 'nextflow.log')
        nf_std_out = os.path.join(path, 'nextflow.stdout')
        iv_std_out = os.path.join(path, 'invoke.stdout')
        out_dir = os.path.join(path, 'output')
        work_dir = os.path.join(path, 'work')

        # Touch instance files and directories
        self.get_or_create_dir(path)
        self.get_or_create_dir(out_dir)
        self.get_or_create_dir(work_dir)

        for targ in [nf_logfile, nf_std_out, iv_std_out]:
            with open(targ, 'a'):
                pass

        # Coerce params accordingly
        params = self._fix_parameters(workflow_name, **params)
        params['out_dir'] = out_dir # Todo: generalise to support 3rd party wfs

        with open(params_file, 'w') as json_file:
            json_file.write(json.dumps(params, indent=4))

        # Launch process
        error = self._start_instance(instance, workflow_target, params_file,
                work_dir, nf_logfile, nf_std_out, iv_std_out, self.database_uri)

        return InstanceCreateResponse(
            created=True, instance=instance.to_dict(), error=error)

    def _start_instance(self, instance, target: str, params_file: str,
        work_dir: str, nf_logfile: str, nf_std_out: str,
        iv_std_out: str, database: str) -> Union[str, None]:

        logfile = open(iv_std_out, 'a')
        stdout = logfile
        stderr = logfile

        command = (
            f'{self.invoker} -i {instance.id} -w {target} -p {params_file} '
            f'-wd {work_dir} -l {nf_logfile} -s {nf_std_out} -d {database} '
            f'-n {self.nextflow}')

        # Ensure the default location for docker on MacOS is available
        env = os.environ.copy()
        env["PATH"] = "/usr/local/bin:" + env["PATH"]

        # Todo: May need to provide some different flags on windows
        # in lieu of start_new_session working
        try:
            proc = subprocess.Popen(command.split(' '), start_new_session=True,
                stdout=stdout, stderr=stderr, close_fds=True, cwd=self.base_dir,
                env=env)
        except FileNotFoundError:
            error = 'Could not launch instance, invocation script not found'
            logfile.write(error)
            instance.status = Statuses.ENCOUNTERED_ERROR
            self.db.commit()
            return error

        instance.pid = proc.pid
        self.db.commit()

    def delete_instance(self, id: str, delete: bool = False) -> bool:
        instance = self._get_instance(id)
        if not instance:
            return False

        # Stop any process
        self._stop_instance(instance)

        # Optionally delete the directory
        if delete:
            try:
                shutil.rmtree(instance.path)
            except FileNotFoundError:
                pass

            # Delete record
            self.db.delete(instance)
            self.db.commit()

        return True

    def _stop_instance(self, instance) -> bool:
        if instance.status != Statuses.LAUNCHED:
            return False

        try:
            os.kill(int(instance.pid), signal.SIGINT)
            return True
        except (OSError, KeyboardInterrupt, TypeError):
            pass

        return False

    #
    # Validation
    #
    def validate(self, workflow, params):
        nfcore = PipelineSchema()
        nfcore.get_schema_path(workflow.path)
        nfcore.load_schema()
        nfcore.input_params.update(params)
        valid, errors = self._validate(nfcore.input_params, nfcore.schema)
        return valid, errors

    def _validate(self, instance, schema, *args, **kwargs):
        errors = {}
        cls = validator_for(schema)
        cls.check_schema(schema)
        validator = cls(schema, *args, **kwargs)
        for error in validator.iter_errors(instance):
            split_message = error.message.split("'")
            errors[split_message[1]] = error.message
        return bool(errors), errors

    #
    # Pathing
    #
    def get_path(self, path: str) -> PathResponse:
        path = self._fix_path(path)
        exists, error = self._check_path(path)
        return PathResponse(path=path, exists=exists, error=error)

    def get_file(self, path: str, contents: bool = False) -> FilePathResponse:
        lines = None
        path = self._fix_path(path)
        exists, error = self._check_path(path)
        if exists and not os.path.isfile(path):
            error = 'Path is not a file'
            return FilePathResponse(
                path=path, exists=exists, error=error, contents=None)
        if exists and contents:
            lines = self.read_file(path)
        return FilePathResponse(
            path=path, exists=exists, error=error, contents=lines)

    def read_file(self, path: str) -> List[str]:
        lines = []
        with open(path) as lf:
            lines = lf.readlines()
            lines = [self._process_line(line) for line in lines]
        return lines

    def _process_line(self, line: str) -> str:
        line = line.rstrip()
        # 7-bit C1 ANSI sequences
        # https://stackoverflow.com/questions/14693701/how-can-i-remove-the-ansi-escape-sequences-from-a-string-in-python
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', line)

    def get_directory(self, path: str, contents: bool = False) -> DirectoryPathResponse:
        items = None
        path = self._fix_path(path)
        exists, error = self._check_path(path)
        if exists and not os.path.isdir(path):
            error = 'Path is not a directory'
            return DirectoryPathResponse(
                path=path, exists=exists, error=error, contents=None)
        if exists and contents:
            items = self.list_dir(path)
        return DirectoryPathResponse(
            path=path, exists=exists, error=error, contents=items)

    def list_dir(self, path: str) -> List[Path]:
        items = []
        abspath = os.path.abspath(path)
        for item in os.listdir(path):
            if item.startswith('.'):
                continue
            item_abspath = os.path.join(abspath, item)
            modified = os.path.getmtime(item_abspath)
            is_dir = os.path.isdir(item_abspath)
            items.append(Path(
                name=item,
                path=item_abspath,
                updated=modified,
                isdir=is_dir))
        return items

    def _fix_path(self, path: str) -> str:
        if not os.path.abspath(path):
            path = os.path.join(self.base_dir, path)
        return path

    def _check_path(self, path) -> Tuple[bool, str]:
        if os.path.exists(path):
            return True, 'Path exists.'
        return False, 'Path does not exist or host cannot see it.'

    def get_or_create_dir(self, path: str) -> Tuple[bool, str]:
        if not os.path.exists(path):
            os.mkdir(path)
            return True, os.path.abspath(path)
        return False, os.path.abspath(path)

    def _fix_parameters(self, workflow_name, **params):
        coerced = {}
        for param_key, param_value in params.items():
            schema = self._get_schema_for_param(workflow_name, param_key)
            fmt = schema.get('format')
            if fmt in ['path', 'file-path', 'directory-path']:
                path = param_value
                if not os.path.isabs(path):
                    path = os.path.join(self.curr_dir, path)
                coerced[param_key] = path
                continue
            coerced[param_key] = param_value
        return coerced

    def _get_schema_for_param(self, workflow_name: str, param_name: str) -> Dict:
        if workflow := self._get_workflow(workflow_name):
            sections = workflow.schema.get('definitions', {})
            for section in sections.values():
                for k, v in section.get('properties', {}).items():
                    if k == param_name:
                        return v
        return {}


class RemoteWorkflowLauncher(WorkflowLauncher):

    def __init__(self, base_dir, workflows_dir,
        ip: str = '0.0.0.0', port: str = '8090'):
        self.ip = ip
        self.port = port

        super().__init__(base_dir, workflows_dir)

    @property
    def instances(self) -> Dict:
        response = requests.get(
            f'http://{self.ip}:{self.port}/instances?uuid={shortuuid.uuid()}')
        return response.json()

    def get_instance(self, id: str) -> Dict:
        response = requests.get(
            f'http://{self.ip}:{self.port}/instances/{id}?uuid={shortuuid.uuid()}')
        return response.json()

    def create_instance(
        self, name: str, workflow_name: str, params: Dict
    ) -> InstanceCreateResponse:
        workflow = self._get_workflow(workflow_name)

        if not workflow or not workflow.target:
            return InstanceCreateResponse(
                created=False, instance={},
                error='Could not create instance, workflow unknown')

        response = requests.post(
            f'http://{self.ip}:{self.port}/instances',
            data=json.dumps({
                'name': name,
                'workflow_name': workflow_name,
                'workflow_target': workflow.target,
                'params': params,
            }),
            headers={
                'Content-type': 'application/json', 
                'Accept': 'text/plain'
            })

        data = response.json()
        return data

    def delete_instance(self, id: str, delete: bool = False) -> bool:
        response = requests.delete(
            f'http://{self.ip}:{self.port}/instances/{id}?delete={delete}')

        data = response.json()
        return data['deleted']

    def get_path(self, path: str) -> PathResponse:
        response = requests.get(
            f'http://{self.ip}:{self.port}/path/{quote_plus(quote_plus(path))}')
        return response.json()

    def get_file(self, path: str, contents: bool = False) -> FilePathResponse:
        _cont = ''
        if contents:
            _cont = f'?contents={shortuuid.uuid()}'
        response = requests.get(
            f'http://{self.ip}:{self.port}/file/{quote_plus(quote_plus(path))}{_cont}')
        return response.json()

    def get_directory(self, path: str, contents: bool = False) -> DirectoryPathResponse:
        _cont = ''
        if contents:
            _cont = f'?contents={shortuuid.uuid()}'
        response = requests.get(
            f'http://{self.ip}:{self.port}/directory/{quote_plus(quote_plus(path))}{_cont}')
        return response.json()


def get_workflow_launcher(
    base_dir, workflows_dir, remote=False, ip=None, port=None):

    if remote:
        kwargs = {'ip': ip, 'port': port}
        for k, v in kwargs.items():
            if v is None:
                kwargs.pop(k)
        return RemoteWorkflowLauncher(base_dir, workflows_dir, **kwargs)

    return WorkflowLauncher(base_dir, workflows_dir)