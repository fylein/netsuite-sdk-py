# netsuite-sdk-py
Python SDK for accessing Netsuite resources
via the SuiteTalk SOAP services.

## Installation

	$ pip install netsuitesdk 

Remark: This python netsuite SDK uses the SOAP/WSDL library [Zeep](https://python-zeep.readthedocs.io/en/master/ "Zeep") which should be automatically be installed when running above pip-command. Otherwise you can run `$ pip install zeep` first.

## Get Started

There are the following options to access a Netsuite account via web services: 
- Either pass credentials (email, password, role and account Id) via login and start a request session
- Pass credentials in the header of each request
- Use token based authentication (within each request)

### Login with credentials

The following code performs a login to a Netsuite account and starts a web service session.

```python
from netsuitesdk import NetSuiteClient

# Initialize the netsuite client instance by passing the application Id
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

### Get Requests
tba

### Passing credentials with requests
tba

### Token based authentication
tba