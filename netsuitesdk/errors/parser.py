from .helpers import replace_numbers, convert_to_camelcase
from .errors import list_of_dicts


def get_entity_values(error_dict, ns_client):
    entity_keys = list(error_dict)
    entity_1 = ns_client.get(convert_to_camelcase(entity_keys[0]), error_dict[entity_keys[0]])
    entity_2 = ns_client.get(convert_to_camelcase(entity_keys[1]), error_dict[entity_keys[1]])

    if entity_keys[1] == 'employee':
        entity_2 = entity_2['email'] if entity_2['email'] else entity_2['firstName'] + " " + entity_2['lastName']
        return entity_1['name'], entity_2

    if entity_keys[0] == 'account':
        entity_1 = entity_1['acctName']
        return entity_1, entity_2['name']

    return entity_1['name'], entity_2['name']


def export_error_parser(error_dict, ns_client, message):

    if list(error_dict) in list_of_dicts:
        entity_1, entity_2 = get_entity_values(error_dict, ns_client)
        entity_keys = list(error_dict)
        parsed_message = replace_numbers(message, entity_1, entity_2, error_dict[entity_keys[0]], error_dict[entity_keys[1]])

    return parsed_message
