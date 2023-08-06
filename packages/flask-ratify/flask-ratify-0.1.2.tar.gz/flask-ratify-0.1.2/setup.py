# -*- coding: utf-8 -*-
"""
    setup
    ~~~~
    flask-ratify is a simple extension to Flask allowing you to ratify (validate) requests
    using jsonschema

    jsonschema is supported for headers, params, and body (json only)

    For schema details used in flask-ratify, see docs/schema.md
    For jsonschema details, check https://pypi.org/project/jsonschema/ and https://json-schema.org/understanding-json-schema/

    :copyright: (c) 2022 by Parvesh Garg.
    :license: Apache Software License 2.0, see LICENSE for more details.
"""

from setuptools import setup
from os.path import join, dirname

setup(
    name='flask-ratify',
    version='0.1.2',
    url='https://github.com/parveshgarg/flask-ratify',
    license='Apache License 2.0',
    author='Parvesh Garg',
    author_email='parveshgarg@gmail.com',
    description="A Flask extension adding a decorator for request validation based on jsonschema",
    long_description=open('README.rst').read(),
    packages=['flask_ratify'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask>=0.9',
        'jsonschema>=4.4.0'
    ],
    tests_require=[
        'nose',
        'packaging'
    ],
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
