"""
For this example script, python-dotenv (pip install python-dotenv)
is used to load authentication parameters from a .env-file
as environment variables. The .env-file would look something like this:

NS_EMAIL = '*****@example.com'
NS_PASSWORD = '*******'
NS_ROLE = '1047'
NS_ACCOUNT = '*********'
NS_APPID = '********-****-****-****-************'

Alternatively, the variables can be set manually in the script.
"""

import os
from dotenv import load_dotenv

from netsuitesdk import NetSuiteClient


def test_create_vendor(ns):
    vendor = ns.Vendor()
    vendor.externalId = 'test_vendor'
    vendor.companyName = 'Another Test Inc.'
    ref = ns.upsert(record=vendor)
    vendor = ns.get('vendor', internalId=ref.internalId)
    print('-'*15)
    ns.print_values(vendor)
    print('-'*15)
    return ref

def test_create_customer(self):
    customer = self.Customer()
    customer.externalId = 'test_customer'
    customer.companyName = 'Test Inc.'
    customer.email = 'test@example.com'
    ref = self.upsert(record=customer)
    customer = ns.get('customer', internalId=ref.internalId)
    print('-'*15)
    ns.print_values(customer)
    print('-'*15)
    return ref

def search_transactions_by_account(ns, internalIds):
    account_refs = []
    for id in internalIds:
        account_refs.append(ns.RecordRef('account', internalId=id))
    account_search_field = ns.SearchMultiSelectField(searchValue=account_refs, operator='anyOf')
    basic_search = ns.basic_search_factory('Transaction', account=account_search_field)
    ns.paginated_search('Transaction', basic_search=basic_search, page_size=20, bodyFieldsOnly=False)

def test_vendor_basic_search(ns):
    records = ns.basic_stringfield_search(type_name='Vendor',
                                attribute='entityId',
                                value='Alexander Valley Vineyards',
                                operator='is')
    return records[0]

