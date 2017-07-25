# -*- coding: utf-8 -*-


from __future__ import print_function
import subprocess

import pytest


def pytest_addoption(parser):
    """
    Define py.test command line options for this plugin.
    """
    group = parser.getgroup('gdeploy-config')
    group.addoption(
        '--gdeploy-configuration-file',
        action='store',
        dest='gdeploy_config_file',
        metavar="CONFIG_FILE",
        help='gdeploy configuration file.',
    )


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
    Pytest fixture which runs given gdeploy configuration file.
    """
    gdeploy_command = get_gdeploy_cmd(
        request.config.option.gdeploy_config_file)
    subprocess.check_call(gdeploy_command)

    setup_marker = request.node.get_marker('ansible_playbook_setup')
    setup_files = []
    teardown_marker = request.node.get_marker('ansible_playbook_teardown')
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
                config_file))
    yield
    # teardown
    for config_file in teardown_files:
        subprocess.check_call(
            get_gdeploy_cmd(
                config_file))
