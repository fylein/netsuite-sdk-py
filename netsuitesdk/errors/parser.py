from .helpers import replace_numbers, convert_to_camelcase
from .errors import list_of_dicts

class ErrorParser():

    def __init__(self, ns_client):
        self.ns_client = ns_client

    def get_entity_values(self, error_dict):

        entity_keys = list(error_dict)
        entity_1 = self.ns_client.get(convert_to_camelcase(entity_keys[0]), error_dict[entity_keys[0]])
        entity_2 = self.ns_client.get(convert_to_camelcase(entity_keys[1]), error_dict[entity_keys[1]])

        if entity_1 and entity_2:
            if entity_keys[1] == 'employee':
                entity_2 = entity_2['email'] if entity_2['email'] else entity_2['firstName'] + " " + entity_2['lastName']
                return entity_1['name'], entity_2

            if entity_keys[0] == 'account':
                entity_1 = entity_1['acctName']
                return entity_1, entity_2['name']

            return entity_1['name'], entity_2['name']


    def export_error_parser(self, error_dict, message):

        parsed_message = message
        if list(error_dict) in list_of_dicts:
            entity_1, entity_2 = self.get_entity_values(error_dict)
            entity_keys = list(error_dict)
            parsed_message = replace_numbers(message, entity_1, entity_2, error_dict[entity_keys[0]], error_dict[entity_keys[1]])

        return parsed_message
