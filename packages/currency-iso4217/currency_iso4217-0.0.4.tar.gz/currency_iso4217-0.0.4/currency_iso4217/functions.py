import json
import pkg_resources


def set_file_path():
    file_path = pkg_resources.resource_stream(__name__, 'currency.json')
    with open(file_path.name, encoding="latin-1") as file:
        data = json.load(file)
    file.close()
    return data


def search_by_code(code):
    data = set_file_path()
    country_currency = {}
    list = []
    for i in data:
        if i['code'].lower() == code.lower():
            country_currency['id'] = i['id']
            country_currency['country'] = i['country']
            country_currency['currency'] = i['currency']
            country_currency['decimals'] = i['decimals']
            list.append(country_currency)
    return(list)


def search_by_country(country):
    data = set_file_path()
    country_currency = {}
    list = []
    for i in data:
        if i['country'].lower() == country.lower():
            country_currency['id'] = i['id']
            country_currency['country'] = i['country']
            country_currency['currency'] = i['currency']
            country_currency['decimals'] = i['decimals']
            list.append(country_currency)
            country_currency = {}
    return(list)


def search_by_currency(currency):
    data = set_file_path()
    country_currency = {}
    list = []
    for i in data:
        if i['currency'].lower() == currency.lower():
            country_currency['id'] = i['id']
            country_currency['country'] = i['country']
            country_currency['currency'] = i['currency']
            country_currency['decimals'] = i['decimals']
            list.append(country_currency)
            country_currency = {}
    return(list)


def show_list():
    data = set_file_path()
    return(data)
