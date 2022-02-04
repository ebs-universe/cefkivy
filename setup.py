#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#===============================================================================
# Written by Rentouch 2013 - http://www.rentouch.ch
#===============================================================================

from setuptools import setup

install_reqs = [
    'cefpython3',
    'kivy',
]

# -----------------------------------------------------------------------------
import cefkivy

# setup
setup(name='cefkivy',
      version=cefkivy.__version__,
      author='Rentouch GmbH',
      author_email='info@rentouch.ch',
      maintainer="Chintalagiri Shashank",
      maintainer_email="shashank@chintal.in",
      url='https://github.com/ebs-universe/cefkivy',

      package_data={'cefkivy': ['images/*.png', '*.kv']},

      packages=['cefkivy', ],

      install_requires=install_reqs,
      entry_points={
            'console_scripts': [
                  'cefkivy-example = cefkivy.example:run'
            ]
      },
)

# -----------------------------------------------------------------------------

