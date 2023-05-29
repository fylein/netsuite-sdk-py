import pytest
from netsuitesdk.errors.helpers import replace_numbers, convert_to_camelcase, export_error_matcher

errors = [
    ('An error occured in a upsert request: Invalid category reference key 1 for entity 12', {'expense_category': 1, 'employee': 12}),
    ('An error occured in a upsert request: Invalid account reference key 1 for subsidiary 12', {'account': 1, 'subsidiary': 12}),
    ('An error occured in a upsert request: Invalid customer reference key 1 for entity 12', {'customer': 1, 'employee': 12}),
    ('An error occured in a upsert request: Invalid location reference key 1 for subsidiary 12', {'location': 1, 'subsidiary': 12}),
    ('An error occured in a upsert request: Invalid department reference key 1 for subsidiary 12', {'department': 1, 'subsidiary': 12}),
    ('An error occured in a upsert request: Invalid currency reference key 1 for subsidiary 12', {'currency': 1, 'subsidiary': 12})
]

def test_replace_number():
    final_string = "An error occured in a upsert request: Invalid category reference key Travel for entity John Doe"
    replaced_string = replace_numbers('An error occured in a upsert request: Invalid category reference key 1 for entity 2', 'Travel', 'John Doe', '1', '2')
    assert final_string == replaced_string


def test_convert_to_camelcase():
    entity_type = 'ExpenseCategory'
    result = convert_to_camelcase('expense_category')
    assert entity_type == result
    
    entity_type = 'Currency'
    result = convert_to_camelcase('currency')
    assert entity_type == result


@pytest.mark.parametrize("input, output", errors)
def test_export_error_matcher(input, output):
    
    result = export_error_matcher(input, 'expense_report')
    assert result == output
