import os
import re
import sys
from setuptools import setup

# Utility function to read from file.
def fread(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def get_version():
    VERSIONFILE="es_stats/_version.py"
    verstrline = fread(VERSIONFILE).strip()
    vsre = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(vsre, verstrline, re.M)
    if mo:
        VERSION = mo.group(1)
    else:
        raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))
    build_number = os.environ.get('ESSTATS_BUILD_NUMBER', None)
    if build_number:
        return VERSION + "b{}".format(build_number)
    return VERSION

def get_install_requires():
    res = ['elasticsearch>=1.6.0' ]
    res.append('dotmap>=1.1.2')
    return res

setup(
    name = "es_stats",
    version = get_version(),
    author = "Aaron Mildenstein",
    author_email = "aaron@mildensteins.com",
    description = "Collect stats from Elasticsearch",
    long_description=fread('README.rst'),
    url = "http://github.com/untergeek/es_stats",
    download_url = "https://github.com/untergeek/es_stats/tarball/v" + get_version(),
    license = "Apache License, Version 2.0",
    install_requires = get_install_requires(),
    keywords = "elasticsearch stats",
    packages = ["es_stats"],
    include_package_data=True,
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
    ],
)
