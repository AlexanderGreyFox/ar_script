import os

from setuptools import setup

lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = lib_folder + '/requirements.txt'
install_requires = []
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()
setup(
    name='exchange_rates',
    version='0.1.0',
    author='Serov Aleksandr',
    author_email='alexserov0@gmail.com',
    packages=['script'],
    description='A script that receives data on exchange rates for the last 30 days and builds a graph based on them.',
    long_description=open('README.md').read(),
    install_requires=install_requires,
    entry_points={
                  'console_scripts': ['exchange_rates=script.script:main'],
                  },
)
