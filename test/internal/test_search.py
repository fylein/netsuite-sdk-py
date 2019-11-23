from netsuitesdk.internal.utils import PaginatedSearch
import logging
import pytest
import time

logger = logging.getLogger(__name__)
 
def test_search_vendor_bills(ns):
    record_type_search_field = ns.SearchStringField(searchValue='VendorBill', operator='contains')
    basic_search = ns.basic_search_factory('Transaction', recordType=record_type_search_field)
    paginated_search = PaginatedSearch(client=ns,
                                        type_name='Transaction',
                                        basic_search=basic_search,
                                        pageSize=5)
    assert len(paginated_search.records) > 0, 'There are no vendor bills'
    logger.debug('record = %s', str(paginated_search.records[0]))

@pytest.mark.parametrize('type_name', ['Account', 'Vendor', 'Department', 'Location', 'Classification'])
def test_search_all(ns, type_name):
    paginated_search = PaginatedSearch(client=ns, type_name=type_name, pageSize=20)
    assert len(paginated_search.records) > 0, f'There are no records of type {type_name}'
    logger.debug('record = %s', str(paginated_search.records[0]))
