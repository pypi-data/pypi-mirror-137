import json
import pkg_resources


def set_file_path():
    file_path = pkg_resources.resource_stream(__name__, 'currency.json')
    print(file_path)
    return file_path


def search_by_code(code):
    file_path = set_file_path()
    with open(file_path, encoding="latin-1") as file:
        data = json.load(file)
    country_currency = {}
    list = []
    for i in data:
        if i['code'].lower() == code.lower():
            country_currency['id'] = i['id']
            country_currency['country'] = i['country']
            country_currency['currency'] = i['currency']
            country_currency['decimals'] = i['decimals']
            list.append(country_currency)
    file.close()
    return(list)


print(search_by_code("clp"))


def search_by_country(country):
    abs_file_path = set_abs_file_path()
    with open(abs_file_path, encoding="utf8") as file:
        data = json.load(file)
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
    file.close()
    return(list)


def search_by_currency(currency):
    abs_file_path = set_abs_file_path()
    with open(abs_file_path, encoding="utf8") as file:
        data = json.load(file)
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
    file.close()
    return(list)


def show_list():
    abs_file_path = set_abs_file_path()
    with open(abs_file_path, encoding="utf8") as file:
        data = json.load(file)
    return(data)
