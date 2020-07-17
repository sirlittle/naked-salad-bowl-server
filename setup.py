#!/usr/bin/env python

from setuptools import find_packages, setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

_conf = dict(
    name='canterbury-corp',
    url='https://github.com/sirlittle/naked-salad-bowl-server',
    author_email='',
    version='0.1.0',
    packages=find_packages(),
    install_requires=required,
    include_package_data=True,
)

if __name__ == '__main__':
    setup(**_conf)
