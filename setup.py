#!/usr/bin/env python

from setuptools import setup

_requirements = []
with open('requirements.txt', 'r') as f:
    _requirements = [line.strip() for line in f]

setup(
    name='brb',
    version='0.1.0',
    author='Software Innovation Bergen, Statoil ASA',
    author_email='fg_gpl@statoil.com',
    description="Everest",
    packages=['brb'],
    package_data={'brb':['share/brb_default_header_names.yml']},
    entry_points={'console_scripts': ['brb = brb.brb:main']},
    install_requires=_requirements,
    url='https://github.com/statoil/brb',
)
