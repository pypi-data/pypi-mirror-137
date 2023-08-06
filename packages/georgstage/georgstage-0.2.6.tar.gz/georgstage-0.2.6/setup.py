# coding=utf-8
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as fi:
    REQUIRE = [
        line.strip() for line in fi.readlines()
        if not line.startswith('#')
    ]

setup(
    name='georgstage',
    version='v0.2.6',
    download_url='https://github.com/skipperkongen/georgstage/archive/refs/tags/v0.2.6.tar.gz',
    licence='MIT',
    author="Pimin Konstantin Kefaloukos",
    author_email="skipperkongen@gmail.com",
    description="Hjælpeprogram til skoleskibet Georg Stage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/skipperkongen/georgstage",
    install_requires=REQUIRE,
    extras_require={'test': ['pytest', 'flake8']},
    packages=find_packages('georgstage'),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
