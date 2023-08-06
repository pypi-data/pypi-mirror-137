import json


def search_by_code(code):
    with open('currency_iso4217/currency.json', encoding="utf8") as file:
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


def search_by_country(country):
    with open('currency_iso4217/currency.json', encoding="utf8") as file:
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
    with open('currency_iso4217/currency.json', encoding="utf8") as file:
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
    with open('currency_iso4217/currency.json', encoding="utf8") as file:
        data = json.load(file)
    return(data)
