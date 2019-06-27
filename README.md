# netsuite-sdk-py
Netsuite-sdk-py is a Python SDK using the SOAP client library zeep(https://python-zeep.readthedocs.io/en/master/) for accessing NetSuite resources via the NetSuite SOAP web service SuiteTalk(http://www.netsuite.com/portal/platform/developer/suitetalk.shtml).

## Installation

	$ pip install netsuitesdk 

Remark: This python NetSuite SDK uses the SOAP/WSDL library [Zeep](https://python-zeep.readthedocs.io/en/master/ "Zeep") which should automatically be installed when running above pip-command. Otherwise you can run `$ pip install zeep` first.

## Get Started

There are the following options to access a NetSuite account via web services: 
- Either pass credentials (email, password, role and account Id) via login and start a request session
- Pass credentials in the header of each request
- Use token based authentication (within each request)

### Login with credentials

The following code performs a login to a NetSuite account and starts a web service session.

```python
from netsuitesdk import NetSuiteClient

# Initialize the NetSuite client instance by passing the application Id
# which will be passed to the request header in the login operation.
ns = NetSuiteClient(caching='sqlite', debug=True)

passport = ns.create_passport(email=NS_EMAIL,
                              password=NS_PASSWORD,
                              role=NS_ROLE,
                              account=NS_ACCOUNT)

# Authenticate the user and start a new webservice session in NetSuite
ns.login(app_id=NS_APPID, passport=passport)

# Make requests. All requests done in this session will be identified
# with the application Id passed to the login operation

ns.logout()
```

To avoid storing the credentials in the python source code file, one can use
python-dotenv (`$ pip install python-dotenv`) to load authentication 
credentials from a .env-file as environment variables. The .env-file would look something like this:

```
NS_EMAIL = '*****@example.com'
NS_PASSWORD = '*******'
NS_ROLE = '1047'
NS_ACCOUNT = '*********'
NS_APPID = '********-****-****-****-************'
```

and the variables could be loaded as follows:

```python
import os
from dotenv import load_dotenv

load_dotenv()
NS_EMAIL = os.getenv("NS_EMAIL")
NS_PASSWORD = os.getenv("NS_PASSWORD")
NS_ROLE = os.getenv("NS_ROLE")
NS_ACCOUNT = os.getenv("NS_ACCOUNT")
NS_APPID = os.getenv("NS_APPID")
```

### Remarks and possible errors regarding authentication
**Note:** NetSuite requires two-factor authentication (2FA) for
all Administrator and other highly privileged roles in all NetSuite accounts.
Instead, you can login with a non-highly privileged role or use
token based authentication (TBA) with your requests. For TBA, see below.

If login fails, a NetSuiteLoginError is thrown. 

For more information about NetSuite authentication, see:
	(https://docs.oracle.com/cloud/latest/netsuitecs_gs/NSATH/NSATH.pdf)

### Passing credentials with requests
tba

### Token based authentication
tba

### Get Request
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
```

## Documentation
Documentation can be found in the docs/_build/html folder (open index.html) and soon in readthedocs.
For contributors: to build the documentation (cd to /docs and) run `make buildapi`
as well as `make html`