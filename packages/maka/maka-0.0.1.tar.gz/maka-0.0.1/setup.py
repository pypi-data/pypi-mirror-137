from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'MAKA Python for online script monitoring and control.'
LONG_DESCRIPTION = 'MAKA Python for online script monitoring and control.'

setup(
    name="maka",
    version=VERSION,
    author="James Runnalls",
    author_email="<runnalls.james@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    license="MIT",
    keywords=['python', 'MAKA', 'monitoring', 'monitor'],
)
