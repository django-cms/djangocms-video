#!/usr/bin/env python
#
# This script requries multiple python versions to be installed.
# You can use pyenv for that.
#
# See: https://github.com/pyenv/pyenv#installation
# For example:
# curl https://pyenv.run | bash
#
# Then setup pyenv shell environment like described here:
# https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv
#
# Install requirements for building python versions:
# https://github.com/pyenv/pyenv/wiki#suggested-build-environment
#
# Now install python versions:
# pyenv install 3.8 3.9 3.10 3.11
#
# Then activate them globaly with the systems default to be still default:
# pyenv global system 3.11 3.10 3.9 3.8
#
# Also pip-tools must be installed for every version of python.
# pip3.8 install pip-tools
# pip3.9 install pip-tools
# pip3.10 install pip-tools
# pip3.11 install pip-tools

from __future__ import annotations

import sys
from os import chdir
from os import environ
from pathlib import Path
from subprocess import run

CONFIG_MATRIX = [
    ["python3.8", "Django>=3.2a1,<3.3", "django-cms>=3.8,<3.9", "py38-django32-cms38.txt",],
    ["python3.8", "Django>=3.2a1,<3.3", "django-cms>=3.9,<3.10", "py38-django32-cms39.txt",],
    ["python3.8", "Django>=3.2a1,<3.3", "django-cms>=3.10,<3.11", "py38-django32-cms310.txt",],

    ["python3.9", "Django>=3.2a1,<3.3", "django-cms>=3.8,<3.9", "py39-django32-cms38.txt",],
    ["python3.9", "Django>=3.2a1,<3.3", "django-cms>=3.9,<3.10", "py39-django32-cms39.txt",],
    ["python3.9", "Django>=3.2a1,<3.3", "django-cms>=3.10,<3.11", "py39-django32-cms310.txt",],

    ["python3.10", "Django>=3.2a1,<3.3", "django-cms>=3.8,<3.9", "py310-django32-cms38.txt",],
    ["python3.10", "Django>=3.2a1,<3.3", "django-cms>=3.9,<3.10", "py310-django32-cms39.txt",],
    ["python3.10", "Django>=3.2a1,<3.3", "django-cms>=3.10,<3.11", "py310-django32-cms310.txt",],
    ["python3.10", "Django>=4.2a1,<5.0", "django-cms>=3.11,<4.0", "py310-django42-cms311.txt",],

    ["python3.11", "Django>=4.2a1,<5.0", "django-cms>=3.11,<4.0", "py311-django42-cms311.txt",],
]

if __name__ == "__main__":
    chdir(Path(__file__).parent)
    environ["CUSTOM_COMPILE_COMMAND"] = "requirements/compile.py"
    environ["PIP_REQUIRE_VIRTUALENV"] = "0"
    common_args = [
        "-m",
        "piptools",
        "compile",
        "--generate-hashes",
        "--allow-unsafe",
    ] + sys.argv[1:]
    # mysqlclient requirements found on each version's "Databases" documentation page:
    # https://docs.djangoproject.com/en/3.0/ref/databases/#mysql-db-api-drivers

    for req in CONFIG_MATRIX:
        cmd = [
            req[0],
            *common_args,
            "--upgrade-package",
            req[1],
            "--upgrade-package",
            req[2],
            "--output-file",
            req[3],
        ]
        print(" ".join(cmd))
        output = run(
            cmd,
            # check=True,
            capture_output=True,
        )
        print(output.stderr.decode('utf-8'))
