#!/usr/bin/env python

"""The setup script."""

import os
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['xnat']

setup_requirements = []

test_requirements = []

setup(
    author="Ralph Brecheisen",
    author_email='r.brecheisen@maastrichtuniversity.nl',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Collection of Python tools for working with XNAT",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='xnatpytools',
    name='xnatpytools',
    packages=find_packages(include=['xnatpytools', 'xnatpytools.*']),
    setup_requires=setup_requirements,
    entry_points={
        'console_scripts': [
            'bulksharing=xnatpytools.bulksharing.bulksharing:main',
        ],
    },
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/rbrecheisen/xnatpytools',
    version=os.environ['VERSION'],
    zip_safe=False,
)
