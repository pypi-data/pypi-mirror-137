#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: Feini Huang
# Mail: 386899557@qq.com
# Created Time:  2022-2-5 19:17:34
#############################################


from setuptools import setup, find_packages

setup(
    name = "ExplainAI",
    version = "0.1.4",
    keywords = ("pip", "ML","XAI", "visualization"),
    description = "explain AI tool",
    long_description = "",
    license = "MIT Licence",

    url = "https://github.com/HuangFeini/ExplainAI",
    author = "Feini Huang",
    author_email = "386899557@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []
)