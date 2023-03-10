from netsuitesdk.internal.utils import PaginatedSearch
import logging
import pytest
import time
from netsuitesdk.internal.exceptions import NetSuiteError

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

def test_search_journal_entries(ns):
    record_type_search_field = ns.SearchStringField(searchValue='JournalEntry', operator='contains')
    basic_search = ns.basic_search_factory('Transaction', recordType=record_type_search_field)
    paginated_search = PaginatedSearch(client=ns,
                                        type_name='Transaction',
                                        basic_search=basic_search,
                                        pageSize=5)
    assert len(paginated_search.records) > 0, 'There are no journal entries'
    logger.debug('record = %s', str(paginated_search.records[0]))

def test_search_expense_reports(ns):
    record_type_search_field = ns.SearchStringField(searchValue='ExpenseReport', operator='contains')
    basic_search = ns.basic_search_factory('Transaction', recordType=record_type_search_field)
    paginated_search = PaginatedSearch(client=ns,
                                        type_name='Transaction',
                                        basic_search=basic_search,
                                        pageSize=5)
    assert len(paginated_search.records) > 0, 'There are no expense reports'
    logger.debug('record = %s', str(paginated_search.records[0]))

def test_search_expense_reports_not_supported(ns):
    record_type_search_field = ns.SearchStringField(searchValue='ExpenseReport', operator='contains')
    with pytest.raises(NetSuiteError) as ex:
        basic_search = ns.basic_search_factory('Transaction1', recordType=record_type_search_field)
    assert "Transaction1 is not a searchable NetSuite type" in str(ex.value.message)

@pytest.mark.parametrize('type_name', ['Account', 'Vendor', 'Department', 'Location', 'Classification', 'Subsidiary', 'Employee'])
def test_search_all(ns, type_name):
    paginated_search = PaginatedSearch(client=ns, type_name=type_name, pageSize=20)
    assert len(paginated_search.records) > 0, f'There are no records of type {type_name}'
    logger.debug('record = %s', str(paginated_search.records[0]))

def test_basic_stringfield_search(ns):
    with pytest.raises(AttributeError) as ex:
        search_entity = ns.basic_stringfield_search("entityId","Amazon","contains")
    assert "'NetSuiteClient' object has no attribute 'entityIdSearchBasic'" in str(ex.value)
