from setuptools import setup, find_packages

from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="yamsl",
    version="0.1.0",
    description="Yet Another Meteo Swiss Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gwrd-ch/yamsl",
    author="gwrd-ch",
    author_email="dev@gwrd.ch",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["yamsl"],
    include_package_data=True,
    install_requires=["aiohttp"]
)