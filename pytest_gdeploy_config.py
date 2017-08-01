# -*- coding: utf-8 -*-


from __future__ import print_function
import os
import subprocess

import pytest


def pytest_addoption(parser):
    """
    Define py.test command line options for this plugin.
    """
    group = parser.getgroup('gdeploy-config')
    group.addoption(
        '--configuration-directory',
        action='store',
        dest='configuration_directory',
        metavar="CONFIG_DIR",
        help='Directory where gdeploy configuration files are stored.',
    )


def pytest_configure(config):
    """
    Validate pytest-gdeploy-config options: when such option is used,
    the given file or directory should exist.

    This check makes the pytest fail immediatelly when wrong path is
    specified, without waiting for the first test case with gdeploy_config
    fixture to fail.
    """
    dir_path = config.getvalue('configuration_directory')
    if dir_path is not None and not os.path.isdir(dir_path):
        msg = (
            "value of --configuration-directory option ({0}) "
            "is not a directory").format(dir_path)
        raise pytest.UsageError(msg)


def get_gdeploy_cmd(gdeploy_file):
    """
    Return process args list for gdeploy run.
    """
    gdeploy_command = [
        'gdeploy',
        '-c',
        gdeploy_file
    ]
    return gdeploy_command


def get_empty_marker_error(marker_type):
    """
    Generate error message for empty marker.
    """
    msg = (
        "no configuration file is specified in "
        "``@pytest.mark.gdeploy_config_{0}`` decorator "
        "of this test case, please add at least one "
        "configuration file file name as a parameter into the marker, eg. "
        "``@pytest.mark.gdeploy_config_{0}('config.conf')``")
    return msg.format(marker_type)


@pytest.fixture
def gdeploy_config(request):
    """
    Pytest fixture which runs given gdeploy configuration file. When gdeploy
    returns nonzero return code, the test case which uses this fixture is not
    executed and ends in ``ERROR`` state.
    """
    setup_marker = request.node.get_marker('gdeploy_config_setup')
    setup_files = []
    teardown_marker = request.node.get_marker('gdeploy_config_teardown')
    teardown_files = []

    if setup_marker is None and teardown_marker is None:
        msg = (
            "no gdeploy configuration is specified for the test case, "
            "please add a decorator like this one "
            "``@pytest.mark.gdeploy_config_setup('config.conf')`` "
            "or "
            "``@pytest.mark.gdeploy_config_teardown('config.conf')`` "
            "for gdeploy_config fixture to know which file to use")
        raise Exception(msg)
    if setup_marker is not None:
        setup_files = setup_marker.args
        if len(setup_marker.args) == 0:
            raise Exception(get_empty_marker_error("setup"))
    if teardown_marker is not None:
        teardown_files = teardown_marker.args
        if len(teardown_marker.args) == 0:
            raise Exception(get_empty_marker_error("teardown"))

    # setup
    for config_file in setup_files:
        subprocess.check_call(
            get_gdeploy_cmd(
                config_file),
            cwd=request.config.option.configuration_directory)
    yield
    # teardown
    for config_file in teardown_files:
        subprocess.check_call(
            get_gdeploy_cmd(
                config_file),
            cwd=request.config.option.configuration_directory)
