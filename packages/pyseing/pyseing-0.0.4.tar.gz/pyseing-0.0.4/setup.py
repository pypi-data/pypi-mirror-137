from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.4'
DESCRIPTION = 'test1'
LONG_DESCRIPTION = 'test1 long description'

# Setting up
setup(
    name="pyseing",
    version=VERSION,
    author="dummy",
    author_email="<aomankit2002@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=['pyseing'],
    package_data={'pyseing': ['pyseing.cpython-38-x86_64-linux-gnu.so']},
    install_requires=[],
    keywords=[],
    classifiers=[]
)
