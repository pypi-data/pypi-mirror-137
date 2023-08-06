# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

VERSION = '0.0.4'
PACKAGE_NAME = 'currency_iso4217'
AUTHOR = 'Marcelo Daniel Iacobucci'
AUTHOR_EMAIL = 'marceloiacobucci@gmail.com'
URL = 'https://gitlab.com/marceloiacobucci'
LICENSE = 'MIT'
DESCRIPTION = 'Librería para buscar y validar divisas conforme listado ISO 4217'
LONG_DESC_TYPE = "text/markdown"


setuptools.setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    packages=setuptools.find_packages(),
    package_data={PACKAGE_NAME: ['currency.json']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

python_requires = '>=3.6',
