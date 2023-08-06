from setuptools import setup, find_namespace_packages

setup(
    name='zipr-core',
    version='0.0.1',
    packages=find_namespace_packages(include=['zipr.*']),
)
