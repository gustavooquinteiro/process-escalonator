import os
from setuptools import setup, find_packages

NAME = 'process-escalonator'
DESCRIPTION = 'Process execution simulator in Python'
URL = 'https://github.com/gustavooquinteiro/process-escalonator'
REQUIRES_PYTHON = '>=3.7.2'

here = os.path.abspath(os.path.dirname(__file__))

requirements = []
with open(os.path.join(here, 'requirements.txt')) as required:
    requirements = required.read().split('\n')

try:
    with open(os.path.join(here, 'README.md'), encoding='utf-8') as readme:
        long_description = '\n'+readme.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setup(
    name=NAME,
    version='1.0.2',
    description=DESCRIPTION,
    url=URL,
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires=REQUIRES_PYTHON,
    license='MIT',
    packages=find_packages(exclude=["tests", "*.tests",
                                    "*.tests.*", "tests.*"]),
    install_requires=requirements,
    include_package_data=True,
    package_data={
        'sample': [
            'images/**']
        },
    zip_safe=False
    )
