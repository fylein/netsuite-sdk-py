
error_reference = {
    "expense_report": {
        'category_reference_error': {
            'regex': r"An error occured in a upsert request: Invalid category reference key \d+ for entity \d+", 
            'keys': ['expense_category', 'employee']
        },
        'account_reference_error': {
            'regex': r"An error occured in a upsert request: Invalid account reference key \d+ for subsidiary \d+", 
            'keys': ['account', 'subsidiary']
        },
        'project_reference_error': {
            'regex': r"An error occured in a upsert request: Invalid customer reference key \d+ for entity \d+", 
            'keys': ['customer', 'employee']
        },
        'location_reference_error': {
            'regex': r"An error occured in a upsert request: Invalid location reference key \d+ for subsidiary \d+", 
            'keys': ['location', 'subsidiary']
        },
        'department_reference_error': {
            'regex':r"An error occured in a upsert request: Invalid department reference key \d+ for subsidiary \d+" , 
            'keys': ['department', 'subsidiary']
        },
        'currency_reference_error': {
            'regex': r"An error occured in a upsert request: Invalid currency reference key \d+ for subsidiary \d+", 
            'keys': ['currency', 'subsidiary']
        }
    },
    "bills": {
        'bill_account_reference_error': {
            'regex': r"An error occured in a upsert request: Invalid account reference key \d+ for subsidiary \d+",
            'keys': ['account', 'subsidiary']
        },
        'location_reference_error': {
            'regex': r"An error occured in a upsert request: Invalid location reference key \d+ for subsidiary \d+", 
            'keys': ['location', 'subsidiary']
        },
        'department_reference_error': {
            'regex':r"An error occured in a upsert request: Invalid department reference key \d+ for subsidiary \d+" , 
            'keys': ['department', 'subsidiary']
        },
        'currency_reference_error': {
            'regex': r"An error occured in a upsert request: Invalid currency reference key \d+ for subsidiary \d+", 
            'keys': ['currency', 'subsidiary']
        },
        'vendor_reference_error': {
            'regex': r"An error occured in a upsert request: Invalid entity reference key \d+ for subsidiary \d+", 
            'keys': ['vendor', 'subsidiary']
        }
    },
    "journal_entry": {
        'location_reference_error': {
            'regex': r"An error occured in a upsert request: Invalid location reference key \d+ for subsidiary \d+", 
            'keys': ['location', 'subsidiary']
        },
        'department_reference_error': {
            'regex':r"An error occured in a upsert request: Invalid department reference key \d+ for subsidiary \d+" , 
            'keys': ['department', 'subsidiary']
        },
        'account_reference_error': {
            'regex': r"An error occured in a upsert request: Invalid account reference key \d+ for subsidiary \d+", 
            'keys': ['account', 'subsidiary']
        },
        'currency_reference_error': {
            'regex': r"An error occured in a upsert request: Invalid currency reference key \d+ for subsidiary \d+", 
            'keys': ['currency', 'subsidiary']
        },
        'project_reference_error': {
            'regex': r"An error occured in a upsert request: Invalid customer reference key \d+ for entity \d+", 
            'keys': ['customer', 'employee']
        },
    }
}


list_of_dicts = [
        ['expense_category', 'employee'], ['account', 'subsidiary'],
        ['customer', 'employee'], ['location', 'subsidiary'],
        ['department', 'subsidiary'], ['currency', 'subsidiary'],
        ['vendor', 'subsdiary']
    ]
