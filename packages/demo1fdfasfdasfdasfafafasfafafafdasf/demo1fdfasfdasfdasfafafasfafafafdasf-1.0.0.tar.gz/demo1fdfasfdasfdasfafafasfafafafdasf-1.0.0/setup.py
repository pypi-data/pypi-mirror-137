#!/usr/bin/env python

import os
from glob import glob
from setuptools import setup, find_packages


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()

setup(  
    name = 'demo1fdfasfdasfdasfafafasfafafafdasf',  
    version = '1.0.0',
    # keywords = ('chinesename',),  
    description = 'Python client for Redis database and key-value store',  
    license = 'MIT License',  
    install_requires = [],  
    # packages = ['chinesename'],  # 要打包的项目文件夹
    include_package_data=True,   # 自动打包文件夹内所有数据
    author = 'yehaiquan',  
    author_email = 'yehaiquan@163.com',
    url = 'https://github.com/freeflyday/demo1',
    # packages = find_packages(include=("*"),),  
)
