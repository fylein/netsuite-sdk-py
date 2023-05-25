from .helpers import decode_project_or_customer_name, replace_numbers


def expense_report_error_parser(error_dict, ns_client, message):
    
    if list(error_dict) == ['category', 'entity']:
        category = ns_client.get('ExpenseCategory', error_dict['category'])['name']
        entity = ns_client.get('Employee', error_dict['entity'])
        entity_name = entity['email'] if entity['email'] else entity['firstName'] + " " + entity['lastName']
        message = replace_numbers(message, category, entity_name, error_dict['category'], error_dict['entity'])
    
    elif list(error_dict) == ['account', 'subsidiary']:
        account = ns_client.get('Account', error_dict['account'])['acctName']
        subsdiary = ns_client.get('Subsidiary', error_dict['subsidiary'])['name']
        message = replace_numbers(message, account, subsdiary, error_dict['account'], error_dict['subsidiary'])
    
    elif list(error_dict) == ['customer', 'entity']:
        customer = ns_client.get('Customer', error_dict['customer'])['entityId']
        customer_name = decode_project_or_customer_name(customer)
        entity = ns_client.get('Employee', error_dict['entity'])
        entity_name = entity['email'] if entity['email'] else entity['firstName'] + " " + entity['lastName']
        message = replace_numbers(message, customer_name, entity_name, error_dict['customer'], error_dict['entity'])
    
    elif list(error_dict) == ['location', 'subsidiary']:
        location = ns_client.get('Location', error_dict['location'])['name']
        subsdiary = ns_client.get('Subsidiary', error_dict['subsidiary'])['name']
        message = replace_numbers(message, location, subsdiary, error_dict['location'], error_dict['subsidiary'])
    
    elif list(error_dict) == ['department', 'subsidiary']:
        department = ns_client.get('Department', error_dict['department'])['name']
        subsdiary = ns_client.get('Subsidiary', error_dict['subsidiary'])['name']
        message = replace_numbers(message, department, subsdiary, error_dict['department'], error_dict['subsidiary'])
    
    elif list(error_dict) == ['currency', 'subsidiary']:
        currency = ns_client.get('Currency', error_dict['currency'])['name']
        subsdiary = ns_client.get('Subsidiary', error_dict['subsidiary'])['name']
        message = replace_numbers(message, currency, subsdiary, error_dict['currency'], error_dict['subsidiary'])
    
    return message
