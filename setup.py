import re
from pathlib import Path
from subprocess import Popen, PIPE, run
from dataclasses import dataclass, field
from typing import List, Callable
import secrets
from os import linesep

c_print: Callable[[str], None] = lambda content: print("\u001B[31m" + content + "\u001B[0m")

REQUIREMENTS: str = 'proj_conda_requirements.txt'
CONTAINER_NAME = re.compile(r"(?P<container_name>\w*)_sec_scan_1", re.DOTALL)

# -------------------------------------Exceptions_------------------------------------------
class CommandException(Exception):
    def __init__(self, errno: int, msg: str):
        self._msg: str = msg
        self._errno: int = errno
        super(CommandException, self).__init__('msg: {}, errno: {}'.format(msg, errno))

    def __reduce__(self):
        return CommandException, (self._msg, self._errno)

    @property
    def msg(self) -> str:
        return self._msg

    @property
    def errno(self) -> int:
        return self._errno


# -------------------------------------DataClasses------------------------------------------

@dataclass
class POutput:
    stdout: str
    stderr: str

    _stdout: str = field(init=False, repr=False)
    _stderr: str = field(init=False, repr=False)

    @property
    def stdout(self) -> str:
        return self._stdout

    @stdout.setter
    def stdout(self, stdout: bytes) -> None:
        self._stdout = ''.join(map(chr, stdout))

    @property
    def stderr(self) -> str:
        return self._stderr

    @stderr.setter
    def stderr(self, stderr: bytes) -> None:
        self._stderr = ''.join(map(chr, stderr))


# -------------------------------------Programm----------------------------------------------

def run_command(cmd: List[str]) -> POutput:
    try:
        p_cmd = Popen(cmd, stderr=PIPE, stdout=PIPE)
    except FileNotFoundError as e:
        err_msg, err_no = f'Command was not found / Sys-Error-msg: {e.strerror}', 1
        raise CommandException(err_no, err_msg)
    return POutput(*p_cmd.communicate())


def verify_docker_install() -> None:
    if run_command(['docker', '--version']).stderr:
        raise CommandException(-1, 'Docker was not found on system!')
    elif run_command(['docker-compose', 'version']).stderr:
        raise CommandException(-1, 'Docker-Compose was not found on system')


def verify_conda_install() -> None:
    if run_command(['conda', 'list']).stderr:
        raise CommandException(-2, 'Please install Anaconda for simplifying project coordination '
                                   '--> https://www.anaconda.com/')


def verify_python_install() -> None:
    if python_cmd := run_command(['python', '--version']):
        if python_cmd.stderr:
            raise CommandException(-2, 'Python was not found on system!')
        elif float(python_cmd.stdout.split(' ')[-1][0:4]) < 3.10:
            raise CommandException(-2, 'Please update Python!')


def setup_conda_env() -> None:
    env_name: str = 'masterProject'
    package_list: List[str] = []
    with Path(Path().absolute() / REQUIREMENTS).open('r', encoding='utf-8') as file:
        for line in (l for l in file if '#' not in l and l):
            package_list.append(line.strip()) if line[0:5] == 'conda' else None

    run_command(['conda', 'create', '--name', env_name, 'python=3.10', '-y'])
    for command in package_list:
        print(f'Installing -> {command.split()[-2]}')
        run_command(command.split())
    run_command(['conda', 'activate', env_name])
    print('Anaconda installed! \nTo activate environment:')
    c_print(f'conda activate {env_name}')


def setup_django_env() -> None:
    print('Writing Django environment variables')
    path: Path = Path(Path().absolute() / 'secScan' / 'secScan' / '.env')
    env_vars: str = f'DEBUG=False{linesep}' \
                    f'SECRET_KEY={secrets.token_urlsafe()}{linesep}'
    with path.open('w', encoding='utf-8') as file:
        file.write(env_vars)


def setup_docker() -> None:
    print('Setting up Docker, this may take a while ~10-15 Minutes')
    run_command(['docker-compose', 'up', '--build', '-d'])


def define_docker_container() -> str:
    docker_ps: POutput = run_command(['docker', 'ps'])
    if match := CONTAINER_NAME.search(docker_ps.stdout):
        return match.group('container_name')
    else:
        raise CommandException(-3, 'Unexpected Error occurred, Docker container was not found!?!?')


if __name__ == '__main__':
    setup_conda_env()
    # try:
    #     verify_docker_install()
    #     verify_conda_install()
    #     setup_conda_env()
    #     setup_django_env()
    #     setup_docker()
    #     print('Install finished!')
    #     c_print('To setup user and database, follow steps...')
    #     print(f'1. docker exec -it {define_docker_container()}_sec_scan_1 bash')
    #     print('2. ./runserver.sh')
    #     print('3. Enter credentials and collect static files')
    #     c_print('Connect to Server at http://localhost:8020/api/v1')
    # except CommandException as e:
    #     print(e.msg)
    #     exit(e.errno)
