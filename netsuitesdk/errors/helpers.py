import re

def decode_project_or_customer_name(name):
    value = name.replace(u'\xa0', ' ')
    value = value.replace('/', '-')
    return value


def replace_numbers(string , replacement1, replacement2, number1, number2):

    replaced_string = re.sub(r'\b({}|{})\b'.format(number1, number2), lambda m: replacement1 if m.group() == number1 else replacement2, string)
    return replaced_string
