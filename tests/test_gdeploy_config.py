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


@pytest.mark.parametrize("dir_value, dir_error", [
    ("/none", "is not a directory"),
    ("/dev", None),
    (None, None),
    ])
@pytest.mark.parametrize("file_value, file_error", [
    ("/none", "is not accessible"),
    ("/dev/zero", None),
    ("zero", None),
    (None, None),
    ])
def test_invalid_options(
        testdir, dir_value, dir_error, file_value, file_error):
    """
    Make sure that pytest reports an ERROR immediatelly when invalid
    options are specified.

    For a file or directory which doesn't exist, "/none" path is used (see
    parametrize decorator).

    For a file or directory which is expected to exist, "/dev/zero" and "/dev"
    values are used (to simplify the setup of the test, but it make the test
    run only on POSIX systems).
    """
    # build ``py.test`` command line arugment list
    args = []
    if dir_value is not None:
        args.append('--configuration-directory={0}'.format(dir_value))
    if file_value is not None:
        args.append('--gdeploy-configuration-file={0}'.format(file_value))
    args.append('-v')

    # run pytest with the following cmd args
    result = testdir.runpytest(*args)

    # build list of expected errors to check in stderr of pytest command
    match_lines = []
    if dir_error is not None:
        match_lines.append('ERROR:*value of *{0}'.format(dir_error))
    # note: when dir_error is detected, pytest ends reporting the problem
    # immediatelly without going on to check configuration file, so
    # it doesn't check for configuration file related error message when
    # issue with directory is detected as well
    if file_error is not None and dir_error is None:
        match_lines.append('ERROR:*value of *{0}'.format(file_error))
    # when path to configuration file is relative, but the path to the
    # directory is not specified
    if file_value == "zero" and dir_value is None:
        match_lines.append('ERROR:*value of *{0}'.format("is not accessible"))

    # fnmatch_lines does an assertion internally
    result.stderr.fnmatch_lines(match_lines)

    # make sure that expected error code is given
    if dir_value is None and file_value is None:
        # this is a case without any gdeploy-config options, equiv. of
        # running ``py.test -v`` in a directory without any tests,
        # so there should be no error
        assert result.ret == 5
    elif dir_value is not None and dir_error is None and file_value is None:
        # case when only the --configuration-directory is specified
        # correctly, without using --gdeploy-configuration-file option,
        # so again, no error
        assert result.ret == 5
    else:
        assert result.ret == 4


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
