from setuptools import setup, find_packages

with open('README.md') as f:
    README = f.read()

with open('LICENSE') as f:
    LICENSE = f.read()

VERSION = '0.0.3'
DESCRIPTION = 'MAKA Python for online script monitoring and control.'

setup(
    name="maka",
    version=VERSION,
    author="James Runnalls",
    author_email="<runnalls.james@gmail.com>",
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    url='https://github.com/JamesRunnalls/river-trace',
    license=LICENSE,
    install_requires=[],
    keywords=['python', 'MAKA', 'monitoring', 'monitor'],
)
