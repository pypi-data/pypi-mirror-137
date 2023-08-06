from setuptools import setup, find_packages

setup(
    name='hyc-utils',
    version='0.1.0',
    packages=find_packages(),
    extras_require={
        'packaging': ['twine'],
        'test': ['pytest'],
    }
)
