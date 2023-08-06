from setuptools import find_packages, setup
setup(
    name='lexoffice-api',
    packages=find_packages(include=['lexoffice']),
    version='0.0.2',
    description='Python library for interacting with the Public API of Lexoffice',
    author='Maik Lorenz',
    install_requires=[],
    test_suite='tests',
)