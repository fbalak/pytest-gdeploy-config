# -*- coding: utf-8 -*-


import pytest


def test_help_message(testdir):
    result = testdir.runpytest(
        '--help',
    )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        'gdeploy-config:',
        '*--configuration-directory=CONFIG_DIR*',
    ])


@pytest.mark.parametrize("dir_value, dir_error", [
    ("/none", "is not a directory"),
    ("/dev", None),
    (None, None),
    ])
def test_invalid_options(
        testdir, dir_value, dir_error):
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

    # fnmatch_lines does an assertion internally
    result.stderr.fnmatch_lines(match_lines)

    # make sure that expected error code is given
    if dir_value is None:
        # this is a case without any gdeploy-config options, equiv. of
        # running ``py.test -v`` in a directory without any tests,
        # so there should be no error
        assert result.ret == 5
    elif dir_value is not None and dir_error is None:
        # case when the --configuration-directory is specified, no error
        assert result.ret == 5
    else:
        assert result.ret == 4
