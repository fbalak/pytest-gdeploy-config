#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-gdeploy-config',
    version='0.1.0',
    author='Filip Balák',
    author_email='fbalak@redhat.com',
    maintainer='Filip Balák',
    maintainer_email='fbalak@redhat.com',
    license='Apache Software License 2.0',
    url='https://github.com/fbalak/pytest-gdeploy-config',
    description='Pytest fixture which runs given gdeploy configuration file.',
    long_description=read('README.rst'),
    py_modules=['pytest_gdeploy_config'],
    install_requires=['pytest>=3.1.1'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
    ],
    entry_points={
        'pytest11': [
            'gdeploy-config = pytest_gdeploy_config',
        ],
    },
)
