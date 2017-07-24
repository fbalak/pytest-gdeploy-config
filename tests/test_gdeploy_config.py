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

def test_gdeploy_config_fixture(testdir):
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
    # create minimal gdeploy configuration file
    server = "localhost"
    config = testdir.makefile(
        ".conf",
        "[hosts]",
        server,
        "",
        "[shell]",
        "action=execute",
        "command=ping -c 1 {}".format(server))
    # run pytest with the following cmd args
    result = testdir.runpytest(
        '--gdeploy-configuration-file={0}'.format(
            os.path.join(config.dirname, config.basename)),
        '-v'
        )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(['*::test_foo PASSED'])
    # make sure that that we get a '1' exit code for the testsuite
    assert result.ret == 0
