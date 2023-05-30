import pytest
from netsuitesdk.errors.parser import ErrorParser

    
def test_export_error_parser(mocker, ns):
    
    mocker.patch(
        'netsuitesdk.errors.parser.ErrorParser.get_entity_values',
        return_value={ 'Travel', 'jhon@gmail.com'}
    )

    parser = ErrorParser(ns)
    result = parser.export_error_parser({'expense_category': '1', 'employee': '22'}, 'An error occured in a upsert request: Invalid category reference key 1 for entity 22')
    assert result == "An error occured in a upsert request: Invalid category reference key Travel for entity jhon@gmail.com"
