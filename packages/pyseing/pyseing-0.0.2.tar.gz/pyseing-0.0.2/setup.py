from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'test1'
LONG_DESCRIPTION = 'test1 long description'

# Setting up
setup(
    name="pyseing",
    version=VERSION,
    author="att1",
    author_email="<aomankit2002@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=[],
    classifiers=[]
)
