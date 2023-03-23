"""Example setup file
"""
from setuptools import find_packages, setup

setup(
    name='py_sik_radio',
    version='0.0.0.1',
    author='UCSD Engineers for Exploration',
    author_email='e4e@eng.ucsd.edu',
    entry_points={
        'console_scripts': [
            'py_sik_radio_config = py_sik_radio.configurator:main',
            'py_sik_radio_server = py_sik_radio.connection_server:main',
            'py_sik_radio_client = py_sik_radio.connection_client:main'
        ]
    },
    packages=find_packages(),
    install_requires=[
        'pyserial',
    ],
    extras_require={
        'dev': [
            'pytest',
            'coverage',
            'pylint',
            'wheel',
        ]
    },
)
