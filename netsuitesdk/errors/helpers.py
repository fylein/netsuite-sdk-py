import re
from .errors import error_reference


def replace_numbers(string , replacement1, replacement2, number1, number2):
    pattern = r"\b({0}|{1})\b".format(number1, number2)
    replaced_string = re.sub(pattern, lambda match: replacement1 if match.group() == str(number1) else replacement2, string)
    return replaced_string


def convert_to_camelcase(word):
    return ''.join(word.title().split('_'))


def export_error_matcher(string, export_type):
    for _, error_data in error_reference[export_type].items():
        if re.match(error_data['regex'], string):
            numbers = re.findall(r'\d+', string)
            return {key: int(number) for key, number in zip(error_data['keys'], numbers)}
    
    return {}
