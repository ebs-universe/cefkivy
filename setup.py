#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#===============================================================================
# Written by Rentouch 2013 - http://www.rentouch.ch
#===============================================================================

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
      author='Rentouch GmbH',
      author_email='info@rentouch.ch',
      maintainer="Chintalagiri Shashank",
      maintainer_email="shashank@chintal.in",
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

