from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.12'
DESCRIPTION = 'test1'
LONG_DESCRIPTION = 'test1 long description'

# Setting up
setup(
    name="pyseing",
    version=VERSION,
    author="dummy",
    author_email="<mao2@jhu.edu>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=[],
    classifiers=[]
)
