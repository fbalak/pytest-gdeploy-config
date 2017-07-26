# -*- coding: utf-8 -*-


import textwrap


import pytest


def test_help_message(testdir):
    result = testdir.runpytest(
        '--help',
    )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        'gdeploy-config:',
        '*--gdeploy-configuration-file=CONFIG_FILE*',
        '*--configuration-directory=CONFIG_DIR*',
    ])


@pytest.mark.parametrize("marker_type", ["setup", "teardown"])
def test_simple(testdir, minimal_gdeploy_config, marker_type):
    """
    Make sure that``gdeploy_config`` fixture is recognized and pytest
    itself is not broken by running very simple configuration file which
    has no side effects.
    """
    # create a temporary pytest test module
    testdir.makepyfile(textwrap.dedent("""\
        import pytest
        @pytest.mark.ansible_playbook_{0}('{1}')
        def test_foo(gdeploy_config):
            assert 1 == 1
        """.format(marker_type, minimal_gdeploy_config.basename)))
    # run pytest with the following cmd args
    result = testdir.runpytest(
        '--gdeploy-configuration-file={0}'.format(
            minimal_gdeploy_config.basename),
        '--configuration-directory={0}'.format(
            minimal_gdeploy_config.dirname),
        '-v'
        )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(['*::test_foo PASSED'])
    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0
