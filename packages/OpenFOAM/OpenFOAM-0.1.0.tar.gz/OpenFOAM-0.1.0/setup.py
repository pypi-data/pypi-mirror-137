#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='OpenFOAM',
    version='0.1.0',
    author='Zhikui Guo',
    author_email='zguo@geomar.de',
    url='https://gitlab.com/hydrothermal-openfoam/pyOpenFOAM',
    description=u'Python API of OpenFOAM, specially for the postprocess and data visualization',
    packages=find_packages(where='.', exclude=('docs_OpenFOAM'), include=('*',)), 
    install_requires=[
        'vtk',
        'matplotlib',
        'numpy',
        'meshio'
        ],
    entry_points={
        'console_scripts': []
    },
    keywords = "OpenFOAM publication figure SCI postprocessing"
)