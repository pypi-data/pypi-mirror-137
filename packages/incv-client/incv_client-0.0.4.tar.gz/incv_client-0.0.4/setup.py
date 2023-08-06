#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="incv_client",
    version="0.0.4",
    author="Oren Zhang",
    url="https://www.incv.net/",
    author_email="oren_zhang@outlook.com",
    description="An API Gateway Tool for INCV",
    packages=["incv_client", "incv_client.tof"],
    install_requires=["requests==2.27.1", "django>=2.2"],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
