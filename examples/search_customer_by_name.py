"""
This example CLI script searches for all customers whose name contains a certain string.
For this, it uses :class:`~netsuitesdk.utils.PaginatedSearch` which in turn
performs NetSuite `search` and `searchMoreWithId` requests and paginates
the results. For the search requests, only one basic search filter is given
which is the name of the customer.

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

def print_customer(customer):
    print('{id}: {first_name} {last_name}   entityId: {entityId}'.format(id=customer.internalId,
                                                      first_name=customer.firstName or '',
                                                      last_name=customer.lastName or '',
                                                      entityId=customer.entityId))

def search_customer_by_name(ns, headers):
    print('Search Customer by name')
    print('-'*15)
    searchValue = input('Please enter search value: ')
    string_field = ns.SearchStringField(searchValue=searchValue, operator='contains')
    basic_search = ns.basic_search_factory('Customer', entityId=string_field)
    paginated_search = PaginatedSearch(client=ns,
                                       type_name='Customer',
                                       basic_search=basic_search,
                                       pageSize=5,
                                       headers=headers)

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
            ns.print_records(records=paginated_search.records, print_func=print_customer)
        elif choice == 'n':
            paginated_search.goto_page(paginated_search.page_index + 1)
        elif choice == 'p':
            paginated_search.goto_page(paginated_search.page_index - 1)
        else:
            print('Invalid choice')

def main():
    ns, headers = init_search()
    search_customer_by_name(ns=ns, headers=headers)

if __name__ == '__main__':
    main()