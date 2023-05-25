import re
from .errors import error_reference


def decode_project_or_customer_name(name):
    value = name.replace(u'\xa0', ' ')
    value = value.replace('/', '-')
    return value


def replace_numbers(string , replacement1, replacement2, number1, number2):
    replaced_string = re.sub(r'\b({}|{})\b'.format(number1, number2), lambda m: replacement1 if m.group() == number1 else replacement2, string)
    return replaced_string


def export_error_matcher(string, export_type):

    if re.match(error_reference[export_type]['category_reference_error'], string):
        numbers = re.findall(r'\d+', string)
        return {"category": numbers[0], "entity": numbers[1]}
    
    if re.match(error_reference[export_type]['account_reference_error'], string):
        numbers = re.findall(r'\d+', string)
        return {"account": numbers[0], "subsidiary": numbers[1]}
    
    if re.match(error_reference[export_type]['project_reference_error'], string):
        numbers = re.findall(r'\d+', string)
        return {"customer": numbers[0], "entity": numbers[1]}
    
    if re.match(error_reference[export_type]['location_reference_error'], string):
        numbers = re.findall(r'\d+', string)
        return {"location": numbers[0], "subsidiary": numbers[1]}
    
    if re.match(error_reference[export_type]['department_reference_error'], string):
        numbers = re.findall(r'\d+', string)
        return {"department": numbers[0], "subsidiary": numbers[1]}
    
    if re.match(error_reference[export_type]['currency_reference_error'], string):
        numbers = re.findall(r'\d+', string)
        return {"currency": numbers[0], "subsidiary": numbers[1]}

    return {}
