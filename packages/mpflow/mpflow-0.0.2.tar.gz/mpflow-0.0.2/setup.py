#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
__author__ = "DannyLee1991"

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='mpflow',
      version='0.0.2',
      description='A multiprocess real-time data process flow',
      author='DannyLee1991',
      author_email='747554505@qq.com',
      url='https://github.com/MaLangTeam/mpflow',
      packages=find_packages(),
      long_description=long_description,
      long_description_content_type="text/markdown",
      license="GPLv3",
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Operating System :: OS Independent"],

      python_requires='>=3.7',
      install_requires=[
          "loguru>=0.6.0",
          "pyyaml>=6.0",
      ]
      )
