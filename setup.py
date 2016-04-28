#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "pyramid>=1.7a2",
]

test_requirements = [
    "pytest",
    "webtest"
]

if os.environ.get("TRAVIS"):
    extras_require = None
else:
    extras_require = {
        'twilio': ["twilio"],
    },

setup(
    name='pyramid_sms',
    version_format='{tag}.{commitcount}+{gitsha}',
    description="SMS service framework for Pyramid",
    long_description=readme + '\n\n' + history,
    author="Mikko Ohtamaa",
    author_email='mikko@opensourcehacker.com',
    url='https://github.com/miohtama/pyramid_sms',
    packages=[
        'pyramid_sms',
    ],
    package_dir={'pyramid_sms':
                 'pyramid_sms'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='pyramid_sms',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    setup_requires=[
        "pytest-runner",
        'setuptools-git >= 0',
        'setuptools-git-version',
    ],
    tests_require=test_requirements,
    extras_require=extras_require,
)

