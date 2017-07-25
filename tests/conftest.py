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
