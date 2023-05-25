
error_reference = {
 "er": 
    {
        "category_reference_error": r"An error occured in a upsert request: Invalid category reference key \d+ for entity \d+",
        "account_reference_error": r"An error occured in a upsert request: Invalid account reference key \d+ for subsidiary \d+",
        "project_reference_error": r"An error occured in a upsert request: Invalid customer reference key \d+ for entity \d+",
        "location_reference_error": r"An error occured in a upsert request: Invalid location reference key \d+ for subsidiary \d+",
        "department_reference_error": r"An error occured in a upsert request: Invalid department reference key \d+ for subsidiary \d+",
        "currency_reference_error": r"An error occured in a upsert request: Invalid currency reference key \d+ for subsidiary \d+",
    }
}

list_of_dicts = [
        ['expense_category', 'employee'], ['account', 'subsidiary'],
        ['customer', 'employee'], ['location', 'subsidiary'],
        ['department', 'subsidiary'], ['currency', 'subsidiary']
    ]
