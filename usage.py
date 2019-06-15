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

def test_create_vendor_bill(ns, externalId, loc_id, vendor_id, bill_account_id, expense_account_id, memo):
    """
    VendorBill type: http://www.netsuite.com/help/helpcenter/en_US/srbrowser/Browser2017_2/schema/record/vendorbill.html
    VendorBillExpense type: http://www.netsuite.com/help/helpcenter/en_US/srbrowser/Browser2017_2/schema/other/vendorbillexpense.html?mode=package
    """

    loc_ref = ns.RecordRef(type='location', internalId=loc_id)
    vendor_ref = ns.RecordRef(type='vendor', internalId=vendor_id)
    bill_account_ref = ns.RecordRef(type='account', internalId=bill_account_id)

    # create a VendorBillExpenseList with two expenses:
    expense_account_ref = ns.RecordRef(type='account', internalId=expense_account_id)
    #customer_ref = ns.RecordRef(type='customer', internalId=1552)
    expense1 = ns.VendorBillExpense(
        account=expense_account_ref,
        #customer=customer_ref,
        amount=10.0,
    )
    expense2 = ns.VendorBillExpense(
        account=expense_account_ref,
        #customer=customer_ref,
        amount=20.0,
    )
    expenseList = ns.VendorBillExpenseList(expense=[expense1, expense2])

    # create the vendor bill:
    vendor_bill = ns.VendorBill(
        externalId=externalId,
        account=bill_account_ref,
        entity=vendor_ref,
        currency=ns.RecordRef(type='currency', internalId='1'),
        location=loc_ref,
        memo=memo,
        expenseList=expenseList,
    )
    return ns.upsert(vendor_bill)

def test_session(ns):
    def next_step():
        inp = input("Press any key to continue or 'q' to quit: ")
        if inp == 'q':
            return False
        return True

    print('Search for vendor `Alexander Valley Vineyards`:')
    vendor_ref = test_vendor_basic_search(ns)
    vendor = ns.get('vendor', internalId=vendor_ref.internalId)
    print('-'*15)
    ns.print_values(vendor)
    print('-'*15)
    if not next_step(): return

    expense_account_id = 68 # Automobile Expense Gas & Oil

    print('Show all transactions of account with id {}:'.format(expense_account_id))
    search_transactions_by_account(ns, internalIds=[expense_account_id])
    if not next_step(): return

    bill_ref = test_create_vendor_bill(ns,
                            externalId='test_bill',
                            loc_id=1,
                            vendor_id=vendor_ref.internalId,
                            bill_account_id=25,
                            expense_account_id=expense_account_id,
                            memo='Test VendorBill upsert')

    bill = ns.get('vendorBill', internalId=bill_ref.internalId)
    print('Created/updated bill:')
    print('-'*15)
    ns.print_values(bill)
    print('-'*15)

def test_login_with_credentials():
    load_dotenv()
    NS_EMAIL = os.getenv("NS_EMAIL")
    NS_PASSWORD = os.getenv("NS_PASSWORD")
    NS_ROLE = os.getenv("NS_ROLE")
    NS_ACCOUNT = os.getenv("NS_ACCOUNT")
    NS_APPID = os.getenv("NS_APPID")

    ns = NetSuiteClient(caching='sqlite', debug=True)

    # Login with user credentials (email, password, role and account)
    passport = ns.create_passport(email=NS_EMAIL,
                                  password=NS_PASSWORD,
                                  role=NS_ROLE,
                                  account=NS_ACCOUNT)
    ns.login(app_id=NS_APPID, passport=passport)

    test_session(ns)

    ns.logout()

def main():
    test_login_with_credentials()

if __name__ == '__main__':
    main()