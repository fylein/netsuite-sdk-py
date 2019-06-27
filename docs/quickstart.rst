Quickstart
===========================================

There are the following options to access a NetSuite account via web services: 

- Either pass credentials (email, password, role and account Id) via login and start a request session

- Pass credentials in the header of each request

- Use token based authentication (within each request)

Login with credentials
------------------------

The following code performs a login to a NetSuite account and starts a web service session: ::

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

To avoid storing the credentials in the python source code file, one can use
python-dotenv (:code:`$ pip install python-dotenv`) to load authentication 
credentials from a .env-file as environment variables. The .env-file would look something like this::

	NS_EMAIL = '*****@example.com'
	NS_PASSWORD = '*******'
	NS_ROLE = '1047'
	NS_ACCOUNT = '*********'
	NS_APPID = '********-****-****-****-************'

and the variables could be loaded as follows: ::

	import os
	from dotenv import load_dotenv

	load_dotenv()
	NS_EMAIL = os.getenv("NS_EMAIL")
	NS_PASSWORD = os.getenv("NS_PASSWORD")
	NS_ROLE = os.getenv("NS_ROLE")
	NS_ACCOUNT = os.getenv("NS_ACCOUNT")
	NS_APPID = os.getenv("NS_APPID")

Remarks and possible errors regarding authentication
------------------------------------------------------

.. note:: NetSuite requires two-factor authentication (2FA) for all Administrator and other highly privileged roles in all NetSuite accounts. Instead, you can login with a non-highly privileged role or use token based authentication (TBA) with your requests. For TBA, see below.

If login fails, a :class:`~netsuitesdk.exceptions.NetSuiteLoginError` is thrown. 

For more information about NetSuite authentication, see: (`<https://docs.oracle.com/cloud/latest/netsuitecs_gs/NSATH/NSATH.pdf>`_)

Passing credentials with requests
-----------------------------------
Every request can either be done inside a session as outlined above or one can
additionally pass a passport in the headers of the request.
This is done as follows: ::

	# First create a passport:
	passport = ns.create_passport(email=NS_EMAIL,
                                  password=NS_PASSWORD,
                                  role=NS_ROLE,
                                  account=NS_ACCOUNT)
    # In the request, pass a `headers` dictionary with passport and applicationInfo:
    headers = {
        'applicationInfo': ns.ApplicationInfo(applicationId=NS_APPID),
        'passport': passport,
    }
    vendor = ns.get('vendor', internalId=1, headers=headers)

.. note:: In the basic examples below for the requests, the headers has to be added if they are used without login

Token based authentication
-----------------------------
tba

Get Request
-------------
A basic example: ::

	# `ns` is a reference to a :class:`~netsuitesdk.client.NetSuiteClient` instance
	vendor = ns.get('vendor', internalId=12)
	ns.print_values(vendor)

Search
-------
To perform a search request, :func:`~netsuitesdk.client.NetSuiteClient.search` can be used.
Further, the SDK provides some utility functions/classes:

- :func:`~netsuitesdk.client.NetSuiteClient.basic_stringfield_search`: A basic example: ::

		# `ns` is a reference to a :class:`~netsuitesdk.client.NetSuiteClient` instance
		records = ns.basic_stringfield_search(type_name='Vendor',
	                                attribute='entityId',
	                                value='Alexander Valley Vineyards',
	                                operator='is')
		print(records[0].internalId)

- :class:`~netsuitesdk.utils.PaginatedSearch`: An utility class that uses the NetSuite requests `search` and `searchMoreWithId` to perform a search and paginate the results. It is used in the following examples: 
	- :doc:`_examples/search_all`
	
	- :doc:`_examples/upsert_vendor_bill` 

Upsert
--------
Basic example: ::

	# `ns` is a reference to a :class:`~netsuitesdk.client.NetSuiteClient` instance
	vendor = ns.Vendor()
	vendor.externalId = 'test_vendor'
	vendor.companyName = 'Another Test Inc.'
	ref = ns.upsert(record=vendor)

See also 
	- :doc:`_examples/upsert_vendor_bill`

UpsertList
-------------
Basic example: ::

	# `ns` is a reference to a :class:`~netsuitesdk.client.NetSuiteClient` instance
	customer1 = ns.Customer(externalId='customer', email='test1@example.com')
	customer2 = ns.Customer(externalId='another_customer', email='test2@example.com')
	ns.upsertList(records=[customer1, customer2])
