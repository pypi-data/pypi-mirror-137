import json
import pkg_resources


def set_file_path():
    file_path = pkg_resources.resource_stream(__name__, 'currency.json')
    with open(file_path.name, encoding="utf-8") as file:
        data = json.load(file)
    file.close()
    return data


def return_data(data, param, value):
    data_list = []
    if value:
        country_currency = {}
        for i in data:
            if i[param].lower() == value.lower():
                country_currency['position'] = i['position']
                country_currency['code'] = i['code']
                country_currency['country'] = i['country']
                country_currency['currency'] = i['currency']
                country_currency['decimals'] = i['decimals']
                data_list.append(country_currency)
                country_currency = {}
    return data_list


def search_by_code(value):
    data = set_file_path()
    data_list = return_data(data, "code", value)
    return data_list


def search_by_country(value):
    data = set_file_path()
    data_list = return_data(data, "country", value)
    return data_list


def search_by_currency(value):
    data = set_file_path()
    data_list = return_data(data, "currency", value)
    return data_list


def search_decimals(value):
    data = set_file_path()
    data_list = return_data(data, "code", value)
    try:
        data = int(data_list[0]['decimals'])
    except:
        data = []
    return data


def show_list():
    data = set_file_path()
    return data
