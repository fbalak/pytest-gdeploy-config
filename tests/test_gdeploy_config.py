# -*- coding: utf-8 -*-


import os
import textwrap


def test_help_message(testdir):
    result = testdir.runpytest(
        '--help',
    )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        'gdeploy-config:',
        '*--gdeploy-configuration-file=CONFIG_FILE*',
    ])


def test_gdeploy_config_fixture(testdir, minimal_gdeploy_config):
    """
    Make sure that``gdeploy_config`` fixture is recognized and pytest
    itself is not broken by running very simple configuration file which
    has no side effects.
    """
    # create a temporary pytest test module
    testdir.makepyfile(textwrap.dedent("""\
        def test_foo(gdeploy_config):
            assert 1 == 1
        """))
    # run pytest with the following cmd args
    result = testdir.runpytest(
        '--gdeploy-configuration-file={0}'.format(
            os.path.join(
                minimal_gdeploy_config.dirname,
                minimal_gdeploy_config.basename)),
        '-v'
        )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(['*::test_foo PASSED'])
    # make sure that that we get a '1' exit code for the testsuite
    assert result.ret == 0
