# BLITSkrieg - a Bitcoin Lightning Integration Test Service
#
# Copyright (C) 2022 hashbeam contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# For a full list of contributors, please see the AUTHORS.md file.
"""Module to bundle BLITSkrieg with setuptools."""

import sys
from contextlib import redirect_stdout, suppress
from importlib import import_module
from io import StringIO
from os import chdir, chmod, linesep, makedirs, path, remove, stat, walk
from pathlib import Path
from shutil import move, rmtree, which
from stat import S_IXGRP, S_IXOTH, S_IXUSR
from subprocess import Popen, TimeoutExpired
from urllib.request import urlretrieve
from zipfile import ZipFile

from pip._vendor.distlib.scripts import ScriptMaker
from pkg_resources import resource_filename
from setuptools import Command, setup
from setuptools.command.build_py import build_py
from setuptools.command.develop import develop
from setuptools.command.sdist import sdist

# directories
B_DIR = 'blitskrieg'
E_DIR = 'examples'
R_DIR = 'reports'
U_DIR = path.sep.join([B_DIR, 'utils'])

# blitskrieg
__version__ = getattr(import_module(B_DIR), '__version__')
PIP_NAME = getattr(import_module(B_DIR + '.settings'), 'PIP_NAME')
PKG_NAME = getattr(import_module(B_DIR + '.settings'), 'PKG_NAME')
PROTO = 'blitskrieg.proto'

# bli
CLI_NAME = 'bli'
CLI_ENTRY = '{0} = {1}.{0}:entrypoint'.format(CLI_NAME, B_DIR)
SHELLS = ['bash', 'zsh']
COMPLETION_SCRIPTS = {}
for SHELL in SHELLS:
    COMPLETION_SCRIPTS[SHELL] = f'complete-{CLI_NAME}-{SHELL}.sh'

# linting
PYLINT_ARGS = [
    '--ignore-patterns=.*_pb2.*\\.py', '--persistent=y', '-f', 'parseable',
    B_DIR
]

# cleanup
CLEANUP_SUFFIXES = [
    '_pb2.py',
    '_pb2_grpc.py',
    '.pyc',
    '.so',
    '.o',
]

# documentation
LONG_DESC = ''
with open('README.md', encoding='utf-8') as f:
    LONG_DESC = f.read()

# data files
DOC = [path.as_posix() for path in Path('.').glob('*.md')] + \
    [path.as_posix() for path in Path('doc').glob('*.md')]
EXAMPLES = [path.as_posix() for path in Path(E_DIR).glob('*')] + \
    [path.sep.join([E_DIR, COMPLETION_SCRIPTS[shell]]) for shell in SHELLS]

# dependencies
DEPS = [
    'click~=7.1.2',
    'docker-compose~=1.28.5',
    'googleapis-common-protos~=1.53.0',
    'grpcio~=1.43.0',
    'boltlight~=2.0.0rc3',
    'PyYAML~=5.4.1',
    'protobuf~=3.19.1',
    'requests~=2.25.1',
]
SETUP_DEPS = [
    'click~=7.1.2',
    'grpcio~=1.43.0',
    'grpcio-tools~=1.43.0',
    'isort~=5.10.1',
    'pylint==2.12.2',
]


def _die(message):
    """Print message to stderr with error code 1."""
    sys.stderr.write(message)
    sys.exit(1)


def _try_rm(tree):
    """Try to remove a directory or file, without failing if missing."""
    with suppress(OSError):
        rmtree(tree)
    with suppress(OSError):
        remove(tree)


def _gen_shell_completion(shell, cli_in_path):
    """Generate CLI completion files for bash and zsh."""
    final_dest = path.join(E_DIR, COMPLETION_SCRIPTS[shell])
    if not which(shell):
        Path(final_dest).touch()
        print(f'Shell {shell} is not installed, creating empty completion '
              'script')
        return
    source = 'source'
    if shell == 'zsh':
        source = 'source_zsh'
    cli_path = CLI_NAME if cli_in_path else path.abspath(CLI_NAME)
    cmd = [
        shell, '-c',
        f'_{CLI_NAME.upper()}_COMPLETE={source} {cli_path} > {final_dest}'
    ]
    proc = Popen(cmd)
    try:
        _, _ = proc.communicate(timeout=10)
        print('Created completion script for', shell)
    except TimeoutExpired:
        proc.kill()
    status = stat(final_dest)
    chmod(final_dest, status.st_mode | S_IXUSR | S_IXGRP | S_IXOTH)


def _gen_proto(opts):
    """Generate python code from given proto file."""
    print('Generating proto files from', opts[-1])
    if not path.exists(opts[-1]):
        _die("Can't find required file: " + opts[-1])
    try:
        from grpc_tools.protoc import main as run_protoc
        if run_protoc(opts) != 0:
            _die('Failed generation of proto files')
    except ImportError:
        _die('Package grpcio-tools isn\'t installed')


def _build_blitskrieg():
    """Download and build BLITSkrieg dependencies and shell completions."""
    opts = [
        '--proto_path=.', '--python_out=.', '--grpc_python_out=.',
        path.sep.join([B_DIR, PROTO])
    ]
    _gen_proto(opts)


def _gen_cli_completion():
    """Generate completion scripts for bli.

    It requires bli's python entrypoint. If it's not in PATH, it creates it.
    To generate completion scripts bli.py must be imported, hence we need
    to add eggs of external packages imported by it (click, protobuf, six,
    grpcio).
    """
    cli_in_path = bool(which(CLI_NAME))
    if not cli_in_path:
        maker = ScriptMaker(B_DIR, '.')
        maker.variants = set(('', ))
        maker.make_multiple((CLI_ENTRY, ))
        buf = None
        with open(CLI_NAME, 'r') as f:
            buf = f.readlines()
        add_egg = "spath.extend(egg)"
        get_egg = "egg = glob(path.join(getcwd(), '.eggs/{}-*.egg'))"
        lines = [
            "from sys import path as spath",
            "from glob import glob",
            "from os import getcwd, path",
            get_egg.format('Click'),
            add_egg,
            get_egg.format('protobuf'),
            add_egg,
            get_egg.format('six'),
            add_egg,
            get_egg.format('grpcio'),
            add_egg,
        ]
        for idx in range(len(lines)):
            lines[idx] = lines[idx] + linesep
        with open(CLI_NAME, 'w') as out:
            inserted = False
            for bufline in buf:
                if not bufline.startswith('#') and not inserted:
                    out.writelines(lines)
                    inserted = True
                out.write(bufline)
    makedirs(E_DIR, exist_ok=True)
    _gen_shell_completion('bash', cli_in_path)
    _gen_shell_completion('zsh', cli_in_path)
    if not cli_in_path:
        _try_rm(CLI_NAME)


class Clean(Command):
    """Clean up generated and downloaded files."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Override default behavior."""
        for (dirpath, _, filenames) in walk('.'):
            _try_rm(path.sep.join([dirpath, '__pycache__']))
            for filename in filenames:
                filepath = path.join(dirpath, filename)
                for suffix in CLEANUP_SUFFIXES:
                    if filepath.endswith(suffix):
                        print(f'Removing file: "{filepath}"')
                        remove(filepath)
        for shell in SHELLS:
            _try_rm(path.sep.join([E_DIR, COMPLETION_SCRIPTS[shell]]))
        for report in Path(R_DIR).glob('*.report'):
            _try_rm(report.as_posix())
        _try_rm(CLI_NAME)
        _try_rm(B_DIR + '.egg-info')
        _try_rm('build')
        _try_rm('dist')
        _try_rm('.coverage')
        _try_rm('.eggs')
        _try_rm('.pytest_cache')


class BuildPy(build_py):
    """Build Python source."""

    def run(self):
        """Override default behavior."""
        _build_blitskrieg()
        _gen_cli_completion()
        build_py.run(self)


class Develop(develop):
    """Define installation in development mode."""

    def run(self):
        """Override default behavior."""
        _build_blitskrieg()
        develop.run(self)
        _gen_cli_completion()


class Lint(Command):
    """Lint code."""

    description = 'lint code with and pylint after in-place build'

    user_options = [
        ('pylint-rcfile=', None, 'path to pylint RC file'),
    ]

    def initialize_options(self):
        """Override default behavior."""
        self.pylint_rcfile = ''

    def finalize_options(self):
        """Override default behavior."""
        if self.pylint_rcfile:
            assert path.exists(self.pylint_rcfile), (
                f'Pylint RC file {self.pylint_rcfile} does not exist')
        else:
            self.pylint_rcfile = '.pylintrc'

    def run(self):
        """Override default behavior."""
        # pylint: disable=import-outside-toplevel
        from pylint.lint import Run as PylintRun

        # pylint: enable=import-outside-toplevel
        makedirs(R_DIR, exist_ok=True)
        print('Running pylint')
        report = ''
        PYLINT_ARGS.insert(0, '--rcfile=' + self.pylint_rcfile)
        try:
            with StringIO() as buf:
                with redirect_stdout(buf):
                    pl_run = PylintRun(PYLINT_ARGS, do_exit=False)
                report = buf.getvalue()
            dest = path.join(R_DIR, 'pylint.report')
            with open(dest, 'w') as f:
                f.write(report)
            score = pl_run.linter.stats.global_note
            print(report)
            if score < 10:
                sys.exit(pl_run.linter.msg_status)
        except OSError:
            print('Failed')


class Sdist(sdist):
    """Create source distribution."""

    def run(self):
        """Override default behavior."""
        _build_blitskrieg()
        _gen_cli_completion()
        sdist.run(self)


setup(name=PIP_NAME,
      version=__version__,
      description='The Bitcoin Lightning Integration Test Service',
      long_description=LONG_DESC,
      long_description_content_type='text/markdown',
      url='https://gitlab.com/hashbeam/blitskrieg',
      author='hashbeam',
      author_email='hashbeam@protonmail.com',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Affero General Public License v3 '
          'or later (AGPLv3+)',
          'Natural Language :: English',
          'Operating System :: MacOS',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Topic :: Other/Nonlisted Topic',
      ],
      keywords='ln lightning network bitcoin integration test boltlight',
      license='AGPLv3',
      packages=[B_DIR, U_DIR],
      include_package_data=True,
      package_data={
          B_DIR: [PROTO],
      },
      data_files=[
          (f'share/doc/{PKG_NAME}', DOC),
          (f'share/doc/{PKG_NAME}/{E_DIR}', EXAMPLES),
      ],
      python_requires='>=3.7',
      install_requires=DEPS,
      setup_requires=SETUP_DEPS,
      entry_points={
          'console_scripts': [
              CLI_ENTRY,
              f'blitskrieg = {B_DIR}.blitskrieg:start',
          ]
      },
      cmdclass={
          'build_py': BuildPy,
          'clean': Clean,
          'develop': Develop,
          'lint': Lint,
          'sdist': Sdist,
      })
