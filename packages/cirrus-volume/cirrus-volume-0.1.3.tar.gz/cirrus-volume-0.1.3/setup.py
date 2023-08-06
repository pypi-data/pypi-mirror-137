import sys
import setuptools
from setuptools import setup, find_packages


__version__ = '0.1.3'


setup(
    name='cirrus-volume',
    version=__version__,
    description='Making happy (well-documented) CloudVolumes',
    author='Nicholas Turner',
    author_email='nturner@zetta.ai',
    url='https://github.com/ZettaAI/cirrus-volume',
    packages=setuptools.find_packages(),
    install_requires=['provenance-toolbox', 'cloud-volume==8.2.0']
)
