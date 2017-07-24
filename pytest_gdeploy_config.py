# -*- coding: utf-8 -*-


from __future__ import print_function
import subprocess

import pytest


def pytest_addoption(parser):
    group = parser.getgroup('gdeploy-config')
    group.addoption(
        '--gdeploy-configuration-file',
        action='store',
        dest='gdeploy_config_file',
        metavar="CONFIG_FILE",
        help='gdeploy configuration file.',
    )


@pytest.fixture
def gdeploy_config(request):
    """
    Pytest fixture which runs given gdeploy configuration file.
    """
    gdeploy_command = [
        'gdeploy',
        '-c',
        request.config.option.gdeploy_config_file,
        ]
    subprocess.check_call(gdeploy_command)
