# netsuite-sdk-py

Netsuite-sdk-py is a Python SDK. It uses the SOAP client library zeep(https://python-zeep.readthedocs.io/en/master/) for accessing NetSuite resources via the NetSuite SOAP web service SuiteTalk(http://www.netsuite.com/portal/platform/developer/suitetalk.shtml), but hides the complexity from the SDK user.

## Installation

	$ pip install netsuitesdk 

## Get Started

There are two ways to access a NetSuite account via web services: 
- Use token-based auth (TBA) (within each request). This is the mechanism supported by this SDK.
- Use email, password, role and account id to login and start a session. This is not supported by this SDK

### Token-based Auth

First, setup TBA credentials using environment variables.

```
# TBA credentials
export NS_ACCOUNT=xxxx
export NS_CONSUMER_KEY=xxxx
export NS_CONSUMER_SECRET=xxxx
export NS_TOKEN_KEY=xxxx
export NS_TOKEN_SECRET=xxxx

```

The following snippet shows how to use TBA to initialize the SDK.

Note: By default the SDK implementation is using the wsdl version '2019_1', if you wish to use other than the default wsdl version, you can pass an optional wsdl_version. The wsdl_version should be in following format: 'year_version' eg. '2023_1' or '2022_2' etc.
From version 3.0.0, the default wsdl_version will be 2024_1.

```python
import os
import itertools
import json
from netsuitesdk import NetSuiteConnection

def connect_tba():
    NS_ACCOUNT = os.getenv('NS_ACCOUNT')
    NS_CONSUMER_KEY = os.getenv('NS_CONSUMER_KEY')
    NS_CONSUMER_SECRET = os.getenv('NS_CONSUMER_SECRET')
    NS_TOKEN_KEY = os.getenv('NS_TOKEN_KEY')
    NS_TOKEN_SECRET = os.getenv('NS_TOKEN_SECRET')
    nc = NetSuiteConnection(
        account=NS_ACCOUNT,
        consumer_key=NS_CONSUMER_KEY,
        consumer_secret=NS_CONSUMER_SECRET,
        token_key=NS_TOKEN_KEY,
        token_secret=NS_TOKEN_SECRET,
        #optional wsdl_version to use version other than '2019_1' 
        wsdl_version='2023_2'
    )
    return nc

nc = connect_tba()

# Use get_all methods to get all objects of certain types
currencies = nc.currencies.get_all()
locations = nc.locations.get_all()
departments = nc.departments.get_all()
classifications = nc.classifications.get_all()
subsidiaries = nc.subsidiaries.get_all()
expense_categories = nc.expense_categories.get_all()
employees = nc.employees.get_all()
all_accounts = list(itertools.islice(nc.accounts.get_all_generator(), 100))
accounts = [a for a in all_accounts if a['acctType'] == '_expense']
vendor_bills = list(itertools.islice(nc.vendor_bills.get_all_generator(), 10))
vendors = list(itertools.islice(nc.vendors.get_all_generator(), 10))
vendor_payments = nc.vendor_payments.get_all()

data = {
  'accounts': accounts,
  'classifications': classifications,
  'departments': departments,
  'locations': locations,
  'currencies': currencies,
  'vendors': vendors,
  'vendor_bills': vendor_bills,
  'subsidiaries': subsidiaries,
  'expense_categories': expense_categories,
  'employees': employees,
  'vendor_payments': vendor_payments
}
with open('/tmp/netsuite.json', 'w') as oj:
	oj.write(json.dumps(data, default=str, indent=2))

# There are also generator methods to iterate over potentially large lists
for c in nc.currencies.get_all_generator():
    print(c)

# Get a specific object
nc.currencies.get(internalId='1')

# Post operation is only supported on vendor_bills, expense_reports, journal_entries and vendor_payments currently (see tests on how to construct vendor bill, expense report and journal entry)
vb = {...}
nc.vendor_bills.post(vb)

er = {...}
nc.expense_reports.post(er)

je = {...}
nc.journal_entries.post(je)

vp = {...}
nc.vendor_payments.post(vp)

### Upsert Files
file = open('receipt.pdf', 'rb').read()

created_folder = nc.folders.post(
    {
        "externalId": 'new-folder',
        "name": 'Receipts'
    }
)

uploaded_file = nc.files.post({
    "externalId": "receipt 1",
    "name": 'receipt.pdf',
    'content': file,
    'fileType': '_PDF',
    "folder": {
                "name": None,
                "internalId": 695,
                "externalId": 'new-folder',
                "type": "folder"
            }
    }
)
```

<!-- ### Password-based Auth

Password-based auth is less preferred. You can set the following environment variables for convenience:

```
export NS_EMAIL=xxxx
export NS_PASSWORD=xxxx
export NS_ROLE=xxx
export NS_ACCOUNT=xxxx
export NS_APPID=xxxx
```

Here's a snippet that shows how the client can be initialized.

```python
import os

from netsuitesdk import NetSuiteClient

def connect_password():
    NS_EMAIL = os.getenv("NS_EMAIL")
    NS_PASSWORD = os.getenv("NS_PASSWORD")
    NS_ROLE = os.getenv("NS_ROLE")
    NS_ACCOUNT = os.getenv("NS_ACCOUNT")
    NS_APPID = os.getenv("NS_APPID")

    ns = NetSuiteClient(account=NS_ACCOUNT)
    ns.login(email=NS_EMAIL, password=NS_PASSWORD, role=NS_ROLE, application_id=NS_APPID)
    return ns

ns = connect_password()

# Do things with ns..

ns.logout()
``` -->

### Remarks and possible errors regarding authentication
**Note:** NetSuite requires two-factor authentication (2FA) for
all Administrator and other highly privileged roles in all NetSuite accounts.
Instead, you can login with a non-highly privileged role or use
token based authentication (TBA) with your requests. For TBA, see below.

If login fails, a NetSuiteLoginError is thrown. 

For more information about NetSuite authentication, see:
	(https://docs.oracle.com/cloud/latest/netsuitecs_gs/NSATH/NSATH.pdf)


<!-- ### Get Request
A basic example (`ns` is a reference to a `NetSuiteClient` instance):
```python
vendor = ns.get('vendor', internalId=ref.internalId)
ns.print_values(vendor)
```

### Search
To perform a search request, use `NetSuite.search`.
The SDK provides some utility functions/classes:

- `basic_stringfield_search`: A basic example (`ns` is a reference to a `NetSuiteClient` instance):
```python
records = ns.basic_stringfield_search(type_name='Vendor',
                                attribute='entityId',
                                value='Alexander Valley Vineyards',
                                operator='is')
print(records[0].internalId)
```

- `PaginatedSearch` (in utils.py):
Its usage can be seen inside the utility function `NetSuiteClient.paginated_search`

### Upsert
Basic example(`ns` is a reference to a `NetSuiteClient` instance):
```python
vendor = ns.Vendor()
vendor.externalId = 'test_vendor'
vendor.companyName = 'Another Test Inc.'
ref = ns.upsert(record=vendor)
```

### UpsertList
Basic example(`ns` is a reference to a `NetSuiteClient` instance):
```python
customer1 = ns.Customer(externalId='customer', email='test1@example.com')
customer2 = ns.Customer(externalId='another_customer', email='test2@example.com')
ns.upsertList(records=[customer1, customer2])
``` -->


## Integration Tests

To run integration tests, you will set both login and TBA credentials for an actual Netsuite account with the right permissions. 
```
# TBA credentials
export NS_ACCOUNT=xxxx
export NS_CONSUMER_KEY=xxxx
export NS_CONSUMER_SECRET=xxxx
export NS_TOKEN_KEY=xxxx
export NS_TOKEN_SECRET=xxxx

python -m pytest test/integration
```
Currently the code coverage is at 90%

To run integration tests on a newly added / modified file

```python
python -m pytest -vv test/integration/test_filename.py; 

```

## Code coverage

To get code coverage report, run this command:

```python
python -m pytest --cov=netsuitesdk

<snipped output>
Name                                                   Stmts   Miss  Cover   
----------------------------------------------------------------------------
netsuitesdk/__init__.py                                    4      0   100%
netsuitesdk/api/__init__.py                                0      0   100%
netsuitesdk/api/accounts.py                                6      0   100%
netsuitesdk/api/adv_inter_company_journal_entries.py       7      0   100%
netsuitesdk/api/base.py                                   90      9    90%   
netsuitesdk/api/classifications.py                         6      0   100%
netsuitesdk/api/currencies.py                             10      0   100%
netsuitesdk/api/custom_record_types.py                    11      0   100%
netsuitesdk/api/custom_records.py                         17      0   100%
netsuitesdk/api/customers.py                              21      0   100%
netsuitesdk/api/departments.py                             6      0   100%
netsuitesdk/api/employees.py                              34      0   100%
netsuitesdk/api/expense_categories.py                      6      0   100%
netsuitesdk/api/expense_reports.py                        58      2    97%   
netsuitesdk/api/files.py                                  23      0   100%
netsuitesdk/api/folders.py                                17      0   100%
netsuitesdk/api/journal_entries.py                        41      0   100%
netsuitesdk/api/locations.py                               6      0   100%
netsuitesdk/api/price_level.py                             6      0   100%
netsuitesdk/api/projects.py                                6      0   100%
netsuitesdk/api/subsidiaries.py                            6      0   100%
netsuitesdk/api/tax_groups.py                              6      0   100%
netsuitesdk/api/tax_items.py                               6      0   100%
netsuitesdk/api/vendor_bills.py                           55      1    98%  
netsuitesdk/api/vendor_payments.py                        46      1    98%   
netsuitesdk/api/vendors.py                                21      0   100%
netsuitesdk/connection.py                                 68      0   100%
netsuitesdk/internal/__init__.py                           0      0   100%
netsuitesdk/internal/client.py                           305     79    74%   
netsuitesdk/internal/constants.py                          4      0   100%
netsuitesdk/internal/exceptions.py                        16      3    81%   
netsuitesdk/internal/netsuite_types.py                     2      0   100%
netsuitesdk/internal/utils.py                             40      4    90%   
----------------------------------------------------------------------------
TOTAL                                                    950     99    90%

```

To get an html report, run this command:

```python
python -m pytest --cov=netsuitesdk --cov-report html:cov_html
```

We want to maintain code coverage of more than 90% for this project at all times.

## Documentation
Documentation can be found in the docs/_build/html folder (open index.html) and soon in readthedocs.
For contributors: to build the documentation (cd to /docs and) run `make buildapi`
as well as `make html`

## Contributions

We are actively accepting contributions. Please mail shwetabh.kumar@fylehq.com if you wish to collaborate on this. (Please write test cases for new additions.)
