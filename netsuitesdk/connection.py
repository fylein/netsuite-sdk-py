from .api import *

class NetSuiteConnection:
    def __init__(account, consumer_key, consumer_secret, token_key, token_secret):
        ns_client = NetsuiteClient(account=account)
        ns_client.connect_tba(consumer_key=consumer_key, consumer_secret=consumer_secret, token_key=token_key, token_secret=token_secret)
        self.accounts = Accounts(ns_client)
        self.classifications = Classifications(ns_client)
        self.departments = Departments(ns_client)
        self.currencies = Currencies(ns_client)
        self.locations = Locations(ns_client)
        self.vendor_bills = VendorBills(ns_client)
        self.vendors = Vendors(ns_client)
