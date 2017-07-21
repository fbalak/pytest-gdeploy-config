# -*- coding: utf-8 -*-

import pytest


def pytest_addoption(parser):
    group = parser.getgroup('gdeploy-config')
    group.addoption(
        '--foo',
        '--gdeploy-configuration-directory',
        action='store',
        dest='gdeploy_config_dir',
        metavar='CONFIG_DIR',
        help='Directory where gdeploy configuration files are stored.'
    )


@pytest.fixture
def bar(request):
    return request.config.option.dest_foo
