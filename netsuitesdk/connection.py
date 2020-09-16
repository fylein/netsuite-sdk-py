from .api.accounts import Accounts
from .api.classifications import Classifications
from .api.departments import Departments
from .api.currencies import Currencies
from .api.locations import Locations
from .api.vendor_bills import VendorBills
from .api.vendors import Vendors
from .api.subsidiaries import Subsidiaries
from .api.journal_entries import JournalEntries
from .api.employees import Employees
from .api.expense_reports import ExpenseReports
from .api.folders import Folders
from .api.files import Files
from .api.expense_categories import ExpenseCategory
from .internal.client import NetSuiteClient


class NetSuiteConnection:
    def __init__(self, account, consumer_key, consumer_secret, token_key, token_secret):
        ns_client = NetSuiteClient(account=account)
        ns_client.connect_tba(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            token_key=token_key,
            token_secret=token_secret
        )
        self.accounts = Accounts(ns_client)
        self.classifications = Classifications(ns_client)
        self.departments = Departments(ns_client)
        self.currencies = Currencies(ns_client)
        self.locations = Locations(ns_client)
        self.vendor_bills = VendorBills(ns_client)
        self.vendors = Vendors(ns_client)
        self.subsidiaries = Subsidiaries(ns_client)
        self.journal_entries = JournalEntries(ns_client)
        self.employees = Employees(ns_client)
        self.expense_reports = ExpenseReports(ns_client)
        self.folders = Folders(ns_client)
        self.files = Files(ns_client)
        self.expense_categories = ExpenseCategory(ns_client)
