from setuptools import setup, find_namespace_packages

setup(
    name='zipr-core',
    version='0.0.3',
    author='Andrew Hoekstra',
    author_email='andrew@pointevector.com',
    url='https://github.com/Pointe-Vector/zipr',
    packages=find_namespace_packages(include=['zipr.*']),
)
