import os
import random
import string

import pytest


pytest_plugins = 'pytester'


@pytest.fixture
def minimal_gdeploy_config(testdir):
    """
    Create minimal gdeploy configuration file that calls ping on localhost.
    """
    server = "localhost"
    config = testdir.makefile(
        ".conf",
        "[hosts]",
        server,
        "",
        "[shell]",
        "action=execute",
        "command=ping -c 1 {}".format(server))
    return config


@pytest.fixture
def testfile_config_generator(testdir):
    """
    Return an object with ``get()`` method to generate a config file which
    creates a test file along with expected path and content.

    This is usefull when one needs one or more config_files with simple and
    easy to check side effect.
    """
    class ConfigGenerator(object):
        _id = 1

        def get(self):
            # create dummy temp file,
            # so that we can check it's ``.dirname`` attribute later
            dummy_file = testdir.makefile(".dummy", "")
            # define file path for a test file which will be created
            # by ansible-config_file run
            test_file_path = os.path.join(
                dummy_file.dirname,
                "test_file.{0}".format(ConfigGenerator._id))
            # generate random content of the test file
            test_file_content = "".join(
                random.choice(string.ascii_letters) for _ in range(15))
            # create ansbile config_file file(which would create file on
            # test_file_path with test_file_content in it)
            config_file = testdir.makefile(
                ".{0}.conf".format(ConfigGenerator._id),
                "[hosts]",
                "localhost",
                "",
                "[shell]",
                "action=execute",
                "command=touch {0}".format(test_file_path),
                "",
                "[update-file]",
                "action=add",
                "dest={0}".format(test_file_path),
                "line={0}".format(test_file_content),
                )
            ConfigGenerator._id += 1
            return config_file, test_file_path, test_file_content

    return ConfigGenerator()


@pytest.fixture
def broken_gdeploy_config(testdir):
    """
    Create minimal gdeploy configuration file with an error in it, so that the
    ``gdeploy_config`` would immediatelly fail when trying to execute it.
    """
    config = testdir.makefile(
        "[hosts]",
        "localhost",
        "",
        "[nothing]",  # here is the problem inserted on purpose
        )
    return config
