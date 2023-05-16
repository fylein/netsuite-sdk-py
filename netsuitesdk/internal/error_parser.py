import re

def decode_project_or_customer_name(name):
    value = name.replace(u'\xa0', ' ')
    value = value.replace('/', '-')
    return value


def replace_numbers(string , replacement1, replacement2, number1, number2):

    replaced_string = re.sub(r'\b({}|{})\b'.format(number1, number2), lambda m: replacement1 if m.group() == number1 else replacement2, string)
    return replaced_string


def expense_report_error_matcher(string):
    category_reference_error = r"An error occured in a upsert request: Invalid category reference key \d+ for entity \d+"
    account_reference_error = r"An error occured in a upsert request: Invalid account reference key \d+ for subsidiary \d+"
    project_reference_error = r"An error occured in a upsert request: Invalid customer reference key \d+ for entity \d+"
    location_reference_error = r"An error occured in a upsert request: Invalid location reference key \d+ for subsidiary \d+"

    if re.match(category_reference_error, string):
        numbers = re.findall(r'\d+', string)
        return {"category": numbers[0], "entity": numbers[1]}
    
    if re.match(account_reference_error, string):
        numbers = re.findall(r'\d+', string)
        return {"account": numbers[0], "subsidiary": numbers[1]}
    
    if re.match(project_reference_error, string):
        numbers = re.findall(r'\d+', string)
        return {"customer": numbers[0], "entity": numbers[1]}
    
    if re.match(location_reference_error, string):
        numbers = re.findall(r'\d+', string)
        return {"location": numbers[0], "subsidiary": numbers[1]}

    return {}
