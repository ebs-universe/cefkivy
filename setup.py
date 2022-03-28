#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from setuptools import setup, find_namespace_packages

from io import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

install_reqs = [
    'cefpython3==66.0',
    'kivy',
    'kivy_garden.ebs.core',
]

URL = 'https://github.com/ebs-universe/kivy_garden.ebs.cefkivy'

# setup
setup(
    name='kivy_garden.ebs.cefkivy',
    description='CEF Browser widget for Kivy',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=URL,
    author='Chintalagiri Shashank',
    author_email='shashank@chintal.in',
    packages=find_namespace_packages(include=['kivy_garden.*']),
    package_data={'kivy_garden.ebs.cefkivy': ['*.kv',
                                              'components/*.js']},
    python_requires='>=3.4, <3.8',
    install_requires=install_reqs,
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
    extras_require={
        'dev': ['pytest>=3.6', 'pytest-cov', 'pytest-asyncio',
                'sphinx_rtd_theme'],
        'ci': ['coveralls', 'pycodestyle', 'pydocstyle'],
    },
    entry_points={},
    classifiers=[
       'Development Status :: 4 - Beta',
       'Intended Audience :: Developers',
       'Topic :: Software Development :: Libraries',
       'License :: OSI Approved :: MIT License',
       'Programming Language :: Python :: 3.5',
       'Programming Language :: Python :: 3.6',
       'Programming Language :: Python :: 3.7',
    ],
    project_urls={
        'Bug Reports': URL + '/issues',
        'Source': URL,
    },
    keywords='Kivy kivy-garden',
)

