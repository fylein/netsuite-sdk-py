from .helpers import replace_numbers, convert_to_camelcase
from .errors import list_of_dicts

class ErrorParser():

    def __init__(self, get_instance):
        self.get_instance = get_instance

    def get_entity_values(self, error_dict):

        entity_keys = list(error_dict)
        object_1 = self.get_instance(convert_to_camelcase(entity_keys[0]), error_dict[entity_keys[0]])
        object_2 = self.get_instance(convert_to_camelcase(entity_keys[1]), error_dict[entity_keys[1]])

        if object_1 and object_2:
            if entity_keys[0] == 'customer' and entity_keys[1] == 'employee':
                return object_1['entityId'], object_2['entityId']

            if entity_keys[1] == 'employee':
                return object_1['name'], object_2['entityId']

            if entity_keys[0] == 'account':
                object_1 = object_1['acctName']
                return object_1, object_2['name']

            if entity_keys[0] == 'vendor':
                return object_1['entityId'], object_2['name']

            return object_1['name'], object_2['name']


    def export_error_parser(self, error_dict, message):

        parsed_message = message
        if list(error_dict) in list_of_dicts:
            object_1, object_2 = self.get_entity_values(error_dict)
            entity_keys = list(error_dict)
            parsed_message = replace_numbers(message, object_1, object_2, error_dict[entity_keys[0]], error_dict[entity_keys[1]])
        return parsed_message
