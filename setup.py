from setuptools import setup

setup(
    name='improvar',
    packages=['improvar'],
    version='0.0.1',
    install_requires=['pysam'],
    entry_points={
        'console_scripts': [
            'improvar = improvar:main',
        ]
    }
)
