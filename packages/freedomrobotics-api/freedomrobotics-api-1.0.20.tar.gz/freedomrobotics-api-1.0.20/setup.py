import re

from setuptools import setup, find_packages


with open("freedomrobotics_api/__init__.py") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name='freedomrobotics-api',
    version=version,
    packages=find_packages(include=['freedomrobotics_api', 'freedomrobotics_api.*']),
    install_requires=['requests'],
)
