#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/8 10:36 AM
# @Author  : chenDing


from setuptools import setup, find_packages

import ssl

ssl._create_default_https_context = ssl._create_unverified_context

setup(
    name='marms',
    version='1.0.2',
    description='my arms',
    packages=find_packages(),
    author='Caturbhuja',
    author_email='caturbhuja@foxmail.com',
    url='',
    install_requires=[
    ],
    license='MIT'
)
