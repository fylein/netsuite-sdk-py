import pytest
from netsuitesdk.errors.parser import export_error_parser

    
def test_export_error_parser(mocker, ns):
    
    mocker.patch(
        'netsuitesdk.errors.parser.get_entity_values',
        return_value={'John Doe', 'Travel'}
    )

    result = export_error_parser({'expense_category': '1', 'employee': '12'}, ns, 'An error occured in a upsert request: Invalid category reference key 1 for entity 12')
    assert result == "An error occured in a upsert request: Invalid category reference key Travel for entity John Doe"
