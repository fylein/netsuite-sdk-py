"""
This example CLI script retrieves all vendors from a NetSuite account.
For this, it uses :class:`~netsuitesdk.utils.PaginatedSearch` which in turn
performs NetSuite `search` and `searchMoreWithId` requests and paginates
the results. For the search requests, no search filters are given, since
we want to retrieve all vendors.

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


def init_search():
    load_dotenv()
    NS_EMAIL = os.getenv("NS_EMAIL")
    NS_PASSWORD = os.getenv("NS_PASSWORD")
    NS_ROLE = os.getenv("NS_ROLE")
    NS_ACCOUNT = os.getenv("NS_ACCOUNT")
    NS_APPID = os.getenv("NS_APPID")

    ns = NetSuiteClient(caching='sqlite', debug=True)

    passport = ns.create_passport(email=NS_EMAIL,
                                  password=NS_PASSWORD,
                                  role=NS_ROLE,
                                  account=NS_ACCOUNT)
    headers = {
        'applicationInfo': ns.ApplicationInfo(applicationId=NS_APPID),
        'passport': passport,
    }

    return ns, headers

def print_vendor(vendor):
    info = []
    info.append('{id}, entityId: {entityId}'.format(id=vendor.internalId, entityId=vendor.entityId))
    if vendor.category:
        info.append('category: {}'.format(vendor.category.name))
    if vendor.companyName:
        info.append('companyName: {}'.format(vendor.companyName))
    if vendor.balance:
        info.append('balance: {}'.format(vendor.balance))
    print(', '.join(info))

def search_all(ns, type_name, headers):
    paginated_search = PaginatedSearch(client=ns, type_name=type_name, pageSize=20, headers=headers)

    def print_overview():
        print('totalRecords: ', paginated_search.total_records)
        print('pageSize: ', paginated_search.page_size)
        print('totalPages: ', paginated_search.total_pages)
        print('pageIndex: ', paginated_search.page_index)
        print('results on page: ', paginated_search.num_records)

    all_options = {
        's': 'show current page',
        'n': 'goto next page',
        'p': 'goto previous page',
        'q': 'quit',
    }

    def user_choice(options):
        info = []
        for option in options:
            key = option
            value = all_options[key]
            info.append('{}: {}'.format(key, value))
        choice = input(', '.join(info) + '\n')
        return choice

    while True:
        print_overview()
        if paginated_search.page_index == 1 and paginated_search.page_index < paginated_search.total_pages:
            choice = user_choice(options=['s', 'n', 'q'])
        elif paginated_search.page_index == paginated_search.total_pages and paginated_search.page_index > 1:
            choice = user_choice(options=['s', 'p', 'q'])
        else:
            choice = user_choice(options=['s', 'p', 'n', 'q'])
        if choice == 'q':
            break
        if choice == 's':
            print_func = None
            if type_name.lower() == 'vendor':
                print_func = print_vendor
            # If print_func is None, :func:`~netsuitesdk.client.NetSuiteClient.print_values` is used
            ns.print_records(records=paginated_search.records, print_func=print_func)
        elif choice == 'n':
            paginated_search.goto_page(paginated_search.page_index + 1)
        elif choice == 'p':
            paginated_search.goto_page(paginated_search.page_index - 1)
        else:
            print('Invalid choice')

def main():
    ns, headers = init_search()
    type_name = input('For which NetSuite type (e.g. Account, Customer, Location, Vendor, ...) do you want to retrieve all records: ')
    type_name = type_name[0].upper() + type_name[1:]
    search_all(ns=ns, type_name=type_name, headers=headers)

if __name__ == '__main__':
    main()