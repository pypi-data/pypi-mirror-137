#!/usr/bin/env/python

from setuptools import setup, find_packages


setup(
    name="seeded-graph-matching",
    author="...",
    classifiers=[],
    packages=find_packages(),
    install_requires=[
        'cython>=0.29.3',
        'tqdm',
        'numpy',
        'pandas',
        'lap05==0.5.0',
        'lapjv>=1.3.1',
    ],
    version="1.0.3"
)
