# coding=utf-8
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='georgstage',
    version='0.2.12',
    download_url='https://github.com/skipperkongen/georgstage/archive/refs/tags/v0.2.12.tar.gz',
    author="Pimin Konstantin Kefaloukos",
    author_email="skipperkongen@gmail.com",
    description="Hjælpeprogram til skoleskibet Georg Stage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/skipperkongen/georgstage",
    install_requires=[
        'numpy~=1.22.0',
        'pandas~=1.4.0',
        'PuLP~=2.6',
        'pyinstaller~=4.9',
    ],
    extras_require={'test': ['pytest', 'flake8']},
    packages=find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
