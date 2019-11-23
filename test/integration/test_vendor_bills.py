import logging
import pytest

logger = logging.getLogger(__name__)

def test_get(nc):
    data = nc.vendor_bills.get_all()
    logger.debug('data = %s', data)
    assert data, 'get all didnt work'

    internal_id = data[0]['internalId']
    data = nc.vendor_bills.get(internalId=internal_id)
    logger.debug('data = %s', data)
    assert data, f'No object with internalId {internal_id}'

def get_location_ref(nc):
    d = next(nc.locations.get_all_generator())
    return nc.locations.get_ref(internalId=d['internalId'])

def get_department_ref(nc):
    d = next(nc.departments.get_all_generator())
    return nc.departments.get_ref(internalId=d['internalId'])

def get_class_ref(nc):
    d = next(nc.classifications.get_all_generator())
    return nc.classifications.get_ref(internalId=d['internalId'])

def get_vendor_ref(nc):
    d = next(nc.vendors.get_all_generator())
    return nc.vendors.get_ref(internalId=d['internalId'])

def get_cat_account_ref(nc):
    # TODO: remove constants
    d = nc.accounts.get(internalId=68)
    return nc.accounts.get_ref(internalId=d['internalId'])

def get_currency_ref(nc):
    d = nc.currencies.get(internalId=1)
    return nc.currencies.get_ref(internalId=d['internalId'])

def get_bill_account_ref(nc):
    return nc.accounts.get_ref(internalId='25')

def test_post(nc):
    vendor_ref = get_vendor_ref(nc)
    bill_account_ref = get_bill_account_ref(nc)
    cat_account_ref = get_cat_account_ref(nc)
    loc_ref = get_location_ref(nc)
    dep_ref = get_department_ref(nc)
    class_ref = get_class_ref(nc)
    currency_ref = get_currency_ref(nc)
    expenses = []

    vbe1 = {}
    vbe1['account'] = cat_account_ref
    vbe1['amount'] = 10.0
    vbe1['department'] = dep_ref
    vbe1['class'] = class_ref
    vbe1['location'] = loc_ref

    expenses.append(vbe1)
    vbe1 = {}
    vbe1['account'] = cat_account_ref
    vbe1['amount'] = 20.0
    vbe1['department'] = dep_ref
    vbe1['class'] = class_ref
    vbe1['location'] = loc_ref

    expenses.append(vbe1)

    bill = { }
    external_id = '1237'
    bill['externalId'] = external_id
    bill['currency'] = currency_ref
    bill['exchangeRate'] = 1.0
    bill['expenseList'] = expenses
    bill['memo'] = 'test memo'
    bill['class'] = class_ref
    bill['location'] = loc_ref
    bill['entity'] = vendor_ref
    logger.debug('posting bill = %s', bill)
    res = nc.vendor_bills.post(bill)
    logger.debug('res = %s', res)
    assert res['externalId'] == external_id, 'External ID does not match'

    bill2 = nc.vendor_bills.get(externalId=external_id)
    logger.debug('bill2 = %s', str(bill2))
    assert (29.99 < bill2['userTotal']) and (bill2['userTotal'] < 30.01), 'Bill total is not 30.0'
