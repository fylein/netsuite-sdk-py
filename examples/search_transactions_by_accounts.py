"""
This example CLI script searches for all transactions (vendor bills) who belong
to one of a list of accounts specified by the user.
For this, it uses :class:`~netsuitesdk.utils.PaginatedSearch` which in turn
performs NetSuite `search` and `searchMoreWithId` requests and paginates
the results. For the search requests, only one basic search filter is given
which is the list of accounts.

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

def search_transactions_by_accounts(ns, headers):
    """
    Searches for all transactions who belong to one of a list of accounts
    specified by the user.
    """

    # First, let user specify all accounts whose transactions should be listed
    internalIds = []

    def add_account(internalId):
        internalIds.append(internalId)

    while True:
        add = input('Add account (y or n)? ')
        if add == 'y' or add == 'Y':
            internalId = input('internalId: ')
            add_account(internalId)
        elif add == 'n' or add == 'N':
            if internalIds:
                break
            else:
                print('Please specify at least one account.')
    account_refs = []
    for id in internalIds:
        account_refs.append(ns.RecordRef('account', internalId=id))

    account_search_field = ns.SearchMultiSelectField(searchValue=account_refs, operator='anyOf')
    basic_search = ns.basic_search_factory('Transaction', account=account_search_field)
    paginated_search = PaginatedSearch(client=ns,
                                       type_name='Transaction',
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
            ns.print_records(records=paginated_search.records)
        elif choice == 'n':
            paginated_search.goto_page(paginated_search.page_index + 1)
        elif choice == 'p':
            paginated_search.goto_page(paginated_search.page_index - 1)
        else:
            print('Invalid choice')

def main():
    ns, headers = init_search()
    search_transactions_by_accounts(ns=ns, headers=headers)

if __name__ == '__main__':
    main()