from legit import __version__
from setuptools import setup, find_packages

# To install the legit-python library, from this directory, run:
#
# python setup.py install
#
# You need to have the setuptools module installed. Read more about setuptools:
# http://pypi.python.org/pypi/setuptools

setup(
    name = "legit",
    version = __version__,
    description = "Legit API client library",
    author = "Legit",
    author_email = "rob@legit.co",
    url = "http://github.com/LegitInc/legit-python/",
    keywords = ["legit"],
    install_requires = ["python-oauth2 >= 1.5.211"],
    packages = find_packages(),
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    long_description = """\
    Python Legit Client Library
    ===========================

    DESCRIPTION
    The Legit client library greatly simplifies making calls against the Legit
    API. See http://www.github.com/LegitInc/legit-python for more on the library
    and http://legitapi.appspot.com for more on the Legit API.

     LICENSE The Twilio Python Helper Library is distributed under the MIT
    License """ )