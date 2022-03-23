#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import setuptools
from setuptools import setup

install_reqs = [
    'cefpython3==66.0',
    'kivy',
]

import cefkivy

# setup
setup(name='cefkivy-ebs',
      version=cefkivy.__version__,
      author='Chintalagiri Shashank',
      author_email='shashank@chintal.in',
      url='https://github.com/ebs-universe/cefkivy',
      packages=setuptools.find_packages(),
      package_data={'cefkivy': ['*.kv',
                                'components/*.js']},
      python_requires='>=3.4, <3.8',
      install_requires=install_reqs,
      entry_points={
            'console_scripts': [
                  'cefkivy-example = cefkivy.example:run'
            ]},
      )

