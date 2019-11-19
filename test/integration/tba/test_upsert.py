from netsuitesdk import PaginatedSearch
import logging
import pytest
import zeep

logger = logging.getLogger(__name__)

def get_location(ns):
    paginated_search = PaginatedSearch(client=ns, type_name='Location', pageSize=20)
    return paginated_search.records[0] 

def test_upsert_vendor_bill(ns):
    vendor_ref = ns.RecordRef(type='vendor', internalId=944)
    bill_account_ref = ns.RecordRef(type='account', internalId=25)
    account_ref = ns.RecordRef(type='account', internalId=68)
    loc = get_location(ns)
    loc_ref = ns.RecordRef(type='location', internalId=loc.internalId)
    expenses = []
    expenses.append(ns.VendorBillExpense(
        account=account_ref,
        amount=10.0))

    expenses.append(ns.VendorBillExpense(
        account=account_ref,
        amount=20.0))

    bill = ns.VendorBill(externalId='1234')
    bill.account = bill_account_ref
    bill.location = loc_ref
    # the vendor for this bill:
    bill.entity = vendor_ref

    bill.currency = ns.RecordRef(type='currency', internalId='1') # US dollar
    bill.exchangerate = 1.0
    bill.expenseList = ns.VendorBillExpenseList(expense=expenses)
    bill.memo = 'test memo'
    record_ref = ns.upsert(bill)
    logger.debug('record_ref = %s', record_ref)
    assert record_ref['externalId'] == '1234', 'External ID does not match'

