"""
Functionality for project setup and various installations. Enter the following
for more details:
    `python setup.py --help`
"""
# pylint:skip-file
from os import path
from setuptools import setup, find_packages

# Read the contents of the README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='autoreduce_db',
    version='22.0.0.dev26',
    description='ISIS Autoreduce',
    author='ISIS Autoreduction Team',
    url='https://github.com/autoreduction/autoreduce-db/',
    install_requires=['autoreduce-utils==22.0.0.dev12', 'Django>=3.2.10'],
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
)
