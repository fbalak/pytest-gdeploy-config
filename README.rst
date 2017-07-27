=====================
pytest-gdeploy-config
=====================

`Pytest`_ `plugin`_ which an easy way to run particular `gdeploy configuration file`_ 
during setup phase of a test case. This is useful when there already are some 
configuration files that can be reused during test setup 

----

Initial structure od this `Pytest`_ plugin was generated with `Cookiecutter`_ 
along with `@hackebrot`_'s `Cookiecutter-pytest-plugin`_ template.


Features
--------

* The plugin provides ``gdeploy-config`` `pytest fixture`_, which allows
  one to run one or more gdeploy configuration files during test setup or tear down.

* It's compatible with both python2 and python3 (playbooks are executed via
  running ``gdeploy-config`` in subprocess instead of using api
  of ansible python module).


Requirements
------------

* gdeploy have to be installed for correct functioning.
  Use version provided by packaging system of your operation system.


Installation
------------

There is no stable release yet, so the only option is to use latest
sources from master branch.

Latest development version 
~~~~~~~~~~~~~~~~~~~~~~~~~~ 

The suggested way to install from sources of current master branch is 
via `python virtual enviroment`_::     

    $ cd pytest-ansible-playbook
    $ virtualenv .env
    $ source .env/bin/activate
    $ pip install -e .
    
Note that you can use `virtualenvwrapper`_ to simplify this workflow.


.. TODO: uncomment the following when the 1st release is done
.. 
.. You can install "pytest-gdeploy-config" via `pip`_ from `PyPI`_::
.. 
..     $ pip install pytest-gdeploy-config


Usage
-----

When the plugin is installed, there are available following command-line
parameters::

    py.test \
        [--configuration-directory <path_to_directory_with_gdeploy_files>] \
        [--gdeploy-configuration-file <name_of_gdeploy_configuration_file>]

Where ``<path_to_directory_with_gdeploy_files>`` is a directory which contains
all gdeploy configuration files that are going to be executed.
A ``gdeploy-config`` process will be able to access the files stored there,
since this directory is set as cwd (current working directory) of the gdeploy 
process.

The ``name_of_configuration_file`` is a `gdeploy configuration file`_ stored
in ``<path_to_directory_with_gdeploy_files>`` or defined by absolute path.



Using gdeploy config fixture
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The plugin provides a single pytest fixture called ``gdeploy_config``. To
specify configuration files to be executed by gdeploy in the fixture, use the
following `pytest markers`_:

* ``@pytest.mark.gdeploy_config_setup('config.conf')``
* ``@pytest.mark.gdeploy_config_teardown('config.conf')``

Note that there can be listed multiple files in the marker if needed, eg.::

    @pytest.mark.gdeploy_config_setup('config1.conf', 'config2.conf')

Both files would be executed in the given order.

Here is an example how to specify 2 files to be run during setup phase
of a test case and one for the teardown::

    @pytest.mark.gdeploy_config_setup('volume.conf', 'config2.conf')
    @pytest.mark.gdeploy_config_teardown('teardown_gluster.conf')
    def test_foo(gdeploy_config):
        """
        Some testing is done here.
        """

While using markers without ``gdeploy_config`` fixture like this is valid::

    @pytest.mark.gdeploy_config_setup('volume.conf', 'config2.conf')
    @pytest.mark.gdeploy_config_teardown('teardown_gluster.conf')
    def test_foo():
        """
        Some testing is done here.
        """

no configuration file is executed that way.

Also note that using a marker without any configuration file parameter or
using the fixture without any marker is not valid and would cause an error.


Contributing
------------

Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `Apache Software License 2.0`_ license, 
"pytest-gdeploy-config" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/fbalak/pytest-gdeploy-config/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`pytest fixture`: http://doc.pytest.org/en/latest/fixture.html
.. _`plugin`: http://doc.pytest.org/en/latest/plugins.html
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.python.org/pypi/pip/
.. _`PyPI`: https://pypi.python.org/pypi
.. _`python virtual enviroment`: https://virtualenv.pypa.io/en/stable/ 
.. _`virtualenvwrapper`: https://virtualenvwrapper.readthedocs.io/en/latest/
.. _`gdeploy configuration file`: http://gdeploy.readthedocs.io/en/latest/conf.html
