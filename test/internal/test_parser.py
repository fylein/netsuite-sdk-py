import pytest
from netsuitesdk.errors.parser import ErrorParser

    
def test_export_error_parser(mocker, ns):
    
    mocker.patch(
        'netsuitesdk.errors.parser.ErrorParser.get_entity_values',
        return_value={'John Doe', 'Travel'}
    )

    parser = ErrorParser(ns)
    result = parser.export_error_parser({'expense_category': '1', 'employee': '12'}, 'An error occured in a upsert request: Invalid category reference key 1 for entity 12')
    assert result == "An error occured in a upsert request: Invalid category reference key Travel for entity John Doe"
