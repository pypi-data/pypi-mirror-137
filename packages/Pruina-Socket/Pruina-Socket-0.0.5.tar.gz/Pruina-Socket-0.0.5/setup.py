# -*- coding: UTF-8 -*-
import os
import time
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='Pruina-Socket',
    version="0.0.5",
    keywords='pruina socket protobuf server client hook multithreading',
    description='Pruina-Socket',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Aminor_z',
    author_email='aminor_z@qq.com',
    url='https://github.com/aminor-z/pruina-socket-python',
    packages=setuptools.find_packages(),
    license='MIT',
    python_requires=">=3.6",
    install_requires=["tqdm", "protobuf"]
)
