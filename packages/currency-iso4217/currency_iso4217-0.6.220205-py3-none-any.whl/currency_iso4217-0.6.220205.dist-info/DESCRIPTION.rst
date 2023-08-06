============================================================
 ISO 4217 currency definitions
============================================================

Package `currency_iso4217` is a self-contained module that allows search currency
by code, country or currency definition returning the corresponding active currency information.

# Pre requirements

Python >=3.6


# Installation

pip install currency-iso4217


# Use

>>> from currency_iso4217 import search_by_code  
>>> search_by_code('CLP')  
>>> [{'id': 42, 'code': 'CLP', 'country': 'Chile', 'currency': 'Peso chileno', 'decimals': '0'}]  


>>> from currency_iso4217 import search_by_country  
>>> search_by_country('Chile')  
>>> [{'id': 41, 'code': 'CLP', 'country': 'Chile', 'currency': 'Unidad de fomento', 'decimals': '4'}, {'id': 42, 'code': 'CLP', 'country': 'Chile', 'currency': 'Peso chileno', 'decimals': '0'}]  


>>> from currency_iso4217 import search_by_currency  
>>> search_by_currency('Peso chileno')  
>>> [{'id': 42, 'code': 'CLP', 'country': 'Chile', 'currency': 'Peso chileno', 'decimals': '0'}]  


>>> from currency_iso4217 import show_list  
>>> show_list()
>>> [...]


Written by Marcelo Daniel Iacobucci. Distributed under Public Domain.


