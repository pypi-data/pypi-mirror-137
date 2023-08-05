#!/usr/bin/env python

import os
from glob import glob
from setuptools import setup, find_packages

setup(  
    name = 'demo1fdfasfdasfdasfafafasfafafafdasf',  
    version = '1.0.1',
    # keywords = ('chinesename',),  
    description = 'Python client for Redis database and key-value store',  
    long_description=open("README.md").read().strip(),
    long_description_content_type="text/markdown",
    keywords=["Redis", "key-value store", "database"],
    license = 'MIT License',  
    install_requires = [],  
    # packages = ['chinesename'],  # 要打包的项目文件夹
    include_package_data=True,   # 自动打包文件夹内所有数据
    author = 'yehaiquan',  
    author_email = 'yehaiquan@163.com',
    url = 'https://github.com/freeflyday/demo1',
    project_urls={
        "Documentation": "https://redis.readthedocs.io/en/latest/",
        "Changes": "https://github.com/redis/redis-py/releases",
        "Code": "https://github.com/redis/redis-py",
        "Issue tracker": "https://github.com/redis/redis-py/issues",
    },
    # packages = find_packages(include=("*"),),  
)
