Por Marcelo Daniel Iacobucci

Librería que permite buscar en el listado ISO 4217 las divisas por código, país o moneda.


💡 Prerequisitos

Python >=3.6


📚 Ejemplo de uso

from currency_iso4217 import search_by_code
from currency_iso4217 import search_by_country
from currency_iso4217 import search_by_currency
from currency_iso4217 import show_list

>>> search_by_code('CLP')
>>> [{'id': 42, 'country': 'Chile', 'currency': 'Peso chileno', 'decimals': '0'}]

>>> search_by_country('Chile')
>>> [{'id': 41, 'country': 'Chile', 'currency': 'Unidad de fomento', 'decimals': '4'}, {'id': 42, 'country': 'Chile', 'currency': 'Peso chileno', 'decimals': '0'}]

>>> search_by_currency('Peso chileno')
>>> [{'id': 42, 'country': 'Chile', 'currency': 'Peso chileno', 'decimals': '0'}]

>>> show_list()
>>> [...]


