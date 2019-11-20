from netsuitesdk import PaginatedSearch
import logging
import pytest
import zeep

logger = logging.getLogger(__name__)

#@pytest.mark.parametrize('type_name', ['Account', 'Vendor', 'Department', 'Location', 'Classification'])
def get_record(ns, type_name):
    paginated_search = PaginatedSearch(client=ns, type_name=type_name, pageSize=20)
    return paginated_search.records[0] 

def get_location(ns):
    return get_record(ns, 'Location')

def get_department(ns):
    return get_record(ns, 'Department')

def get_class(ns):
    return get_record(ns, 'Classification')

def get_vendor(ns):
    return get_record(ns, 'Vendor')

def get_category_account(ns):
    return get_record(ns, 'Account')

def test_upsert_vendor_bill(ns):
    vendor_ref = ns.RecordRef(type='vendor', internalId=get_vendor(ns).internalId)
    bill_account_ref = ns.RecordRef(type='account', internalId=25)
    cat_account_ref = ns.RecordRef(type='account', internalId=get_category_account(ns).internalId)
    loc_ref = ns.RecordRef(type='location', internalId=get_location(ns).internalId)
    dep_ref = ns.RecordRef(type='department', internalId=get_department(ns).internalId)
    class_ref = ns.RecordRef(type='classification', internalId=get_department(ns).internalId)
    expenses = []

    vbe1 = ns.VendorBillExpense()
    vbe1.account = cat_account_ref
    vbe1.amount = 10.0
    vbe1.department = dep_ref
    vbe1['class'] = class_ref
    vbe1.location = loc_ref

    expenses.append(vbe1)
    vbe1 = ns.VendorBillExpense()
    vbe1.account = cat_account_ref
    vbe1.amount = 10.0
    vbe1.department = dep_ref
    vbe1['class'] = class_ref
    vbe1.location = loc_ref

    expenses.append(vbe1)

    bill = ns.VendorBill(externalId='1234')
    bill.currency = ns.RecordRef(type='currency', internalId='1') # US dollar
    bill.exchangerate = 1.0
    bill.expenseList = ns.VendorBillExpenseList(expense=expenses)
    bill.memo = 'test memo'
    record_ref = ns.upsert(bill)
    logger.debug('record_ref = %s', record_ref)
    assert record_ref['externalId'] == '1234', 'External ID does not match'

    bill2 = ns.get(recordType='vendorBill', externalId='1234')
    logger.debug('bill2 = %s', str(bill2))
    assert (29.99 < bill2['userTotal']) and (bill2['userTotal'] < 30.01), 'Bill total is not 30.0'
