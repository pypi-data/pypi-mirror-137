from setuptools import setup, find_packages
import pygame

VERSION = '0.0.2'
DESCRIPTION = 'a package to make games'
LONG_DESCRIPTION = 'a package to make games using the pygame package but simplifeid (because i barely know how to use it)'

setup(
    name='pygamedev',
    version=VERSION,
    author='jortpower2009 (Jort Vlaming)',
    author_email="<vlamingjort@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['pygame'],
    keywords=['python', 'game', 'dev', 'gamedev']
)