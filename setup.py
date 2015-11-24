# -*- coding: utf-8 -*-
import re
import ast

from setuptools import setup, find_packages

_version_re = re.compile(r'__version__\s+=\s+(.*)')
with open('backcheck/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='backcheck',
    author='Aaron Toth',
    version=version,
    url='https://github.com/aaront/backcheck',
    description='An asynchronous NHL.com data scraper',
    long_description=open('README.rst').read(),
    install_requires=[
        'lxml',
        'click',
        'aiohttp',
        'python-dateutil'
    ],
    test_suite="tests",
    include_package_data=True,
    packages=find_packages(),
    package_data={'': ['LICENSE']},
    package_dir={'backcheck': 'backcheck'},
    license='Apache 2.0',
    entry_points='''
        [console_scripts]
        backcheck=backcheck.cli:main
    ''',
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries'
    ),
)
