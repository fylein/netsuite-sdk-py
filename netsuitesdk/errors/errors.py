
error_reference = {
 "er": 
    {
        'category_reference_error': {'regex': r"An error occured in a upsert request: Invalid category reference key \d+ for entity \d+", 'keys': ['expense_category', 'employee']},
        'account_reference_error': {'regex': r"An error occured in a upsert request: Invalid account reference key \d+ for subsidiary \d+", 'keys': ['account', 'subsidiary']},
        'project_reference_error': {'regex': r"An error occured in a upsert request: Invalid customer reference key \d+ for entity \d+", 'keys': ['customer', 'employee']},
        'location_reference_error': {'regex': r"An error occured in a upsert request: Invalid location reference key \d+ for subsidiary \d+", 'keys': ['location', 'subsidiary']},
        'department_reference_error': {'regex':r"An error occured in a upsert request: Invalid department reference key \d+ for subsidiary \d+" , 'keys': ['department', 'subsidiary']},
        'currency_reference_error': {'regex': r"An error occured in a upsert request: Invalid currency reference key \d+ for subsidiary \d+", 'keys': ['currency', 'subsidiary']}
    }
}

list_of_dicts = [
        ['expense_category', 'employee'], ['account', 'subsidiary'],
        ['customer', 'employee'], ['location', 'subsidiary'],
        ['department', 'subsidiary'], ['currency', 'subsidiary']
    ]
