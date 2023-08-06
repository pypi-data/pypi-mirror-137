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
    name='autoreduce_utils',
    version='22.0.0.dev12',
    description='ISIS Autoreduce',
    author='ISIS Autoreduction Team',
    url='https://github.com/autoreduction/autoreduce-utils/',
    install_requires=[
        'attrs==21.4.0',
        'gitpython<=3.1.26',
        'python-icat==0.20.1',
        'suds-py3==1.4.5.0',
        'stomp.py==7.0.0',
    ],
    packages=find_packages(),
    package_data={"autoreduce_utils": ["test_credentials.ini"]},
    entry_points={"console_scripts": ["autoreduce-creds-migrate = autoreduce_utils.migrate_credentials:main"]},
    long_description=long_description,
    long_description_content_type='text/markdown',
)
