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

        @pytest.mark.gdeploy_config_{0}('{1}')
        def test_foo(gdeploy_config):
            assert 1 == 1
        """.format(marker_type, minimal_gdeploy_config.basename)))
    # run pytest with the following cmd args
    result = testdir.runpytest(
        '--configuration-directory={0}'.format(
            minimal_gdeploy_config.dirname),
        '-v'
        )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(['*::test_foo PASSED'])
    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


@pytest.mark.parametrize("marker_type", ["setup", "teardown"])
def test_checkfile(
        testdir, testfile_config_generator, marker_type):
    """
    Make sure that ``gdeploy_config`` fixture actually executes
    given configuration file.
    """
    gdeploy_file, test_file_path, test_file_content = \
        testfile_config_generator.get()
    # create a temporary pytest test module
    testdir.makepyfile(textwrap.dedent("""\
        import pytest

        @pytest.mark.gdeploy_config_{0}('{1}')
        def test_foo(gdeploy_config):
            assert 1 == 1

        @pytest.mark.gdeploy_config_{0}('{1}')
        def test_bar(gdeploy_config):
            assert 1 == 0
        """.format(marker_type, gdeploy_file.basename)))
    # run pytest with the following cmd args
    result = testdir.runpytest(
        '--configuration-directory={0}'.format(gdeploy_file.dirname),
        '-v',
        )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_foo PASSED',
        '*::test_bar FAILED',
        ])
    # check that test_file has been created
    with open(test_file_path, 'r') as test_file_object:
        content = test_file_object.read()
        assert content == test_file_content + "\n"
    # make sure that that we get a '1' exit code for the testsuite
    assert result.ret == 1


@pytest.mark.parametrize("marker_type", ["setup", "teardown"])
def test_two_checkfile(
        testdir, testfile_config_generator, marker_type):
    """
    Make sure that ``gdeploy_config`` fixture actually executes
    both config files specified in the marker decorator.
    """
    config_file_1, filepath_1, content_1 = testfile_config_generator.get()
    config_file_2, filepath_2, content_2 = testfile_config_generator.get()
    # create a temporary pytest test module
    testdir.makepyfile(textwrap.dedent("""\
        import pytest

        @pytest.mark.gdeploy_config_{0}('{1}', '{2}')
        def test_1(gdeploy_config):
            assert 1 == 1
        """.format(
            marker_type, config_file_1.basename, config_file_2.basename)))
    # check assumption of this test case, if this fails, we need to rewrite
    # this test case so that both config_file files ends in the same directory
    assert config_file_1.dirname == config_file_2.dirname
    # run pytest with the following cmd args
    result = testdir.runpytest(
        '--configuration-directory={0}'.format(config_file_1.dirname),
        '-v',
        )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(['*::test_1 PASSED'])
    # check that test_file has been created
    for file_path, exp_content in zip(
            (filepath_1, filepath_2),
            (content_1, content_2)):
        with open(file_path, 'r') as test_file_object:
            content = test_file_object.read()
            assert content == exp_content + "\n"
    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_teardown_checkfile(testdir, testfile_config_generator):
    """
    Make sure that ``gdeploy_config`` fixture actually executes
    setup config_file during setup, and then teardown config_file during
    teardown.

    This is done by making the check in the temporary pytest module
    (see testdir.makepyfile call), which makes sure that:

    * setup temporary file exists
    * teardown temporary file doesn't exist
    """
    # setup config_file
    config_file_1, filepath_1, content_1 = testfile_config_generator.get()
    # teardown config_file
    config_file_2, filepath_2, content_2 = testfile_config_generator.get()
    # create a temporary pytest test module
    testdir.makepyfile(textwrap.dedent("""\
        import pytest

        @pytest.mark.gdeploy_config_setup('{setup_config_file}')
        @pytest.mark.gdeploy_config_teardown('{teardown_config_file}')
        def test_proper_teardown(gdeploy_config):
            with open('{setup_file_path}', 'r') as test_file_object:
                content = test_file_object.read()
                assert content == '{setup_exp_content}' + "\\n"
            with pytest.raises(IOError):
                open('{teardown_file_path}', 'r')
        """.format(
            setup_config_file=config_file_1.basename,
            teardown_config_file=config_file_2.basename,
            setup_file_path=filepath_1,
            setup_exp_content=content_1,
            teardown_file_path=filepath_2,
            )))
    # check assumption of this test case, if this fails, we need to rewrite
    # this test case so that both config_file files ends in the same directory
    assert config_file_1.dirname == config_file_2.dirname
    # run pytest with the following cmd args
    result = testdir.runpytest(
        '--configuration-directory={0}'.format(config_file_1.dirname),
        '-v',
        )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(['*::test_proper_teardown PASSED'])
    # check that test_file has been created
    for file_path, exp_content in zip(
            (filepath_1, filepath_2),
            (content_1, content_2)):
        with open(file_path, 'r') as test_file_object:
            content = test_file_object.read()
            assert content == exp_content + "\n"
    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_missing_mark(testdir, minimal_gdeploy_config):
    """
    Make sure that test cases ends in ERROR state when a test case is not
    marked with ``@pytest.mark.gdeploy_config_setup('config_file.conf')``.
    """
    # create a temporary pytest test module
    testdir.makepyfile(textwrap.dedent("""\
        import pytest

        def test_foo(gdeploy_config):
            assert 1 == 1
        """))
    # run pytest with the following cmd args
    result = testdir.runpytest(
        '--configuration-directory={0}'.format(minimal_gdeploy_config.dirname),
        '-v',
        )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_foo ERROR',
        ])
    # make sure that that we get a '1' exit code for the testsuite
    assert result.ret == 1


@pytest.mark.parametrize("marker_type", ["setup", "teardown"])
def test_empty_mark(testdir, minimal_gdeploy_config, marker_type):
    """
    Make sure that test cases ends in ERROR state when a test case is
    marked with empty marker decorator
    (``@pytest.mark.gdeploy_config_setup()``).
    """
    # create a temporary pytest test module
    testdir.makepyfile(textwrap.dedent("""\
        import pytest

        @pytest.mark.gdeploy_config_{0}()
        def test_foo(gdeploy_config):
            assert 1 == 1
        """.format(marker_type)))
    # run pytest with the following cmd args
    result = testdir.runpytest(
        '--configuration-directory={0}'.format(minimal_gdeploy_config.dirname),
        '-v',
        )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_foo ERROR',
        ])
    # make sure that that we get a '1' exit code for the testsuite
    assert result.ret == 1


@pytest.mark.parametrize("marker_type", ["setup", "teardown"])
def test_gdeploy_error(testdir, broken_gdeploy_config, marker_type):
    """
    Make sure that test cases ends in ERROR state when ``gdeploy_config``
    fixture fails (because of ansible reported error).
    """
    # create a temporary pytest test module
    testdir.makepyfile(textwrap.dedent("""\
        import pytest

        @pytest.mark.gdeploy_config_{0}('{1}')
        def test_foo(gdeploy_config):
            assert 1 == 1

        @pytest.mark.gdeploy_config_{0}('{1}')
        def test_bar(gdeploy_config):
            assert 1 == 0
        """.format(marker_type, broken_gdeploy_config.basename)))
    # run pytest with the following cmd args
    result = testdir.runpytest(
        '--configuration-directory={0}'.format(broken_gdeploy_config.dirname),
        '-v',
        )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        'Sorry! Looks like the format of configuration file *\
is not something we could read! '
        ])
    # make sure that that we get a '1' exit code for the testsuite
    assert result.ret == 1
