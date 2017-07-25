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

* TODO

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
