#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Bolsuite Web API connector for Python
# https://github.com/crapher/bolsuite.python.git

"""Bolsuite Web API connector for Python"""

from setuptools import setup, find_packages
import io
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with io.open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='bolsuite.python',
    version="0.1",
    description='Python connector to Bolsuite Web API',
    long_description=long_description,
    url='https://github.com/crapher/bolsuite.python',
    author='Diego Degese',
    author_email='ddegese@gmail.com',
    license='Apache',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',

        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Office/Business :: Financial',
        'Topic :: Office/Business :: Financial :: Investment',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    platforms=['any'],
    keywords='pandas, bolsuite',
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'examples']),
    install_requires=['pandas>=1.0.0', 'numpy>=1.18.1', 'requests>=2.21.0'],
    entry_points={
        'console_scripts': [
            'sample=sample:main',
        ],
    },
)
