#!/usr/bin/env python3

import setuptools;

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read();

setuptools.setup(
    name="csotools-serverquery",
    version="0.3.0",
    author="AnggaraNothing",
    author_email="anggarayamap@protonmail.com",
    description="Query GoldSource and CSO servers for server info, players and more.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/an-cso-projects/cso-py-csotools-serverquery",
    packages=setuptools.find_packages(where="."),
    license="MIT License",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment"
    ],
    python_requires=">=3.7"
);
