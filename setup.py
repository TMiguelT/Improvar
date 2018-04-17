from setuptools import setup, find_packages

setup(
    name='vcffake',
    packages=['vcffake'],
    version='0.0.1',
    install_requires=['pysam'],
    entry_points={
        'console_scripts': [
            'vcffake = vcffake:main',
        ]
    }
)
