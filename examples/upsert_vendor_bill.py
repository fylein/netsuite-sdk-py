"""
This example CLI script shows how to start a session with passport credentials
and how to create a vendor bill with expenses.
For a reference of the attributes of VendorBill see
    http://www.netsuite.com/help/helpcenter/en_US/srbrowser/Browser2017_2/script/record/vendorbill.html
For a reference of the attributes of VendorBillExpense see
    http://www.netsuite.com/help/helpcenter/en_US/srbrowser/Browser2017_2/schema/other/vendorbillexpense.html?mode=package


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
from netsuitesdk import NetSuiteClient, PaginatedSearch


def upsert_vendor_bill(ns):
    print('Upsert a vendor bill with expenses')
    print('-'*30)

    new_bill = False
    while True:
        externalId = input('externalId of VendorBill: ')
        bill = ns.get('vendorBill', externalId=externalId)
        if bill is None:
            inp = input('VendorBill with externalId {} does not exist yet. Do you want to create a new record? (y or n) '.format(externalId))
            if inp == 'y':
                new_bill = True
                break
        else:
            ns.print_values(bill)
            inp = input('VendorBill with externalId {} already exists. Do you want to update the record? (y or n) '.format(externalId))
            if inp == 'y':
                break

    # Ask for location
    loc_ref = None
    while loc_ref is None:
        loc = input('Please enter a location (either internalId or string for search): ')
        try:
            int(loc)
        except ValueError:
            rec = ns.basic_stringfield_search('Location', 'name', loc, operator='contains')
            if rec is None:
                print('Did not find location with name containing {}'.format(loc))
            elif len(rec) > 1:
                print('Found more than one result:')
                for result in rec:
                    print('internalId={}: {}'.format(result.internalId, result.name))
            else:
                print('Found: {}'.format(rec[0].name))
                loc_ref = ns.RecordRef(type='location', internalId=rec[0].internalId)
        else:
            loc_ref = ns.RecordRef(type='location', internalId=loc)

    vendor_ref = ns.RecordRef(type='vendor', internalId=944)
    bill_account_ref = ns.RecordRef(type='account', internalId=25)
    account_ref = ns.RecordRef(type='account', internalId=68)

    expenses = []

    def add_expense(amount):
        expenses.append(ns.VendorBillExpense(
            account=account_ref,
            #customer=customer_ref,
            amount=amount))

    while True:
        add = input('Add expense (y or n)? ')
        if add == 'y' or add == 'Y':
            amount = input('Amount: ')
            add_expense(amount)
        elif add == 'n' or add == 'N':
            break

    bill = ns.VendorBill(externalId=externalId)
    bill.account = bill_account_ref

    # the vendor for this bill:
    bill.entity = vendor_ref

    bill.currency = ns.RecordRef(type='currency', internalId='1') # US dollar
    bill.exchangerate = 1.0
    bill.location = loc_ref
    if new_bill or expenses:
        bill.expenseList = ns.VendorBillExpenseList(expense=expenses)
    bill.memo = input('Memo for the bill: ')

    record_ref = ns.upsert(bill)
    if new_bill:
        print('New vendor bill:')
    else:
        print('Updated vendor bill:')
    ns.print_values(record_ref)
    inp = input('Do you want to read a verbose description of the vendor bill? (y or n)')
    if inp == 'y':
        bill = ns.get('vendorBill', externalId=externalId)
        ns.print_values(bill)

def start_session():
    load_dotenv()
    NS_EMAIL = os.getenv("NS_EMAIL")
    NS_PASSWORD = os.getenv("NS_PASSWORD")
    NS_ROLE = os.getenv("NS_ROLE")
    NS_ACCOUNT = os.getenv("NS_ACCOUNT")
    NS_APPID = os.getenv("NS_APPID")

    ns = NetSuiteClient()

    # Login with user credentials (email, password, role and account)
    passport = ns.create_passport(email=NS_EMAIL,
                                  password=NS_PASSWORD,
                                  role=NS_ROLE,
                                  account=NS_ACCOUNT)
    try:
        ns.login(applicationId=NS_APPID, passport=passport)
        upsert_vendor_bill(ns)
    finally:
        ns.logout()

def main():
    start_session()

if __name__ == '__main__':
    main()