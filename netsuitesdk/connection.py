from .api.accounts import Accounts
from .api.billing_account import BillingAccount
from .api.classifications import Classifications
from .api.credit_memos import CreditMemos
from .api.departments import Departments
from .api.currencies import Currencies
from .api.locations import Locations
from .api.vendor_bills import VendorBills
from .api.vendor_credits import VendorCredits
from .api.vendors import Vendors
from .api.subsidiaries import Subsidiaries
from .api.usage import Usage
from .api.journal_entries import JournalEntries
from .api.employees import Employees
from .api.expense_reports import ExpenseReports
from .api.folders import Folders
from .api.files import Files
from .api.customers import Customers
from .api.projects import Projects
from .api.expense_categories import ExpenseCategory
from .api.custom_lists import CustomLists
from .api.custom_segments import CustomSegments
from .api.custom_record_types import CustomRecordTypes
from .api.custom_records import CustomRecords
from .api.vendor_payments import VendorPayments
from .api.invoices import Invoices
from .api.terms import Terms
from .api.tax_items import TaxItems
from .api.tax_groups import TaxGroups
from .internal.client import NetSuiteClient


class NetSuiteConnection:
    def __init__(self, account, consumer_key, consumer_secret, token_key, token_secret,
                 caching=True, caching_timeout=2592000, caching_path=None,
                 search_body_fields_only=True, page_size: int = 100):
        ns_client = NetSuiteClient(account=account, caching=caching, caching_timeout=caching_timeout,
                                   caching_path=caching_path, search_body_fields_only=search_body_fields_only,
                                   page_size=page_size)
        ns_client.connect_tba(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            token_key=token_key,
            token_secret=token_secret
        )
        self.client = ns_client
        self.accounts = Accounts(ns_client)
        self.billing_accounts = BillingAccount(ns_client)
        self.classifications = Classifications(ns_client)
        self.departments = Departments(ns_client)
        self.currencies = Currencies(ns_client)
        self.locations = Locations(ns_client)
        self.vendor_bills = VendorBills(ns_client)
        self.vendor_credits = VendorCredits(ns_client)
        self.vendors = Vendors(ns_client)
        self.subsidiaries = Subsidiaries(ns_client)
        self.journal_entries = JournalEntries(ns_client)
        self.employees = Employees(ns_client)
        self.expense_reports = ExpenseReports(ns_client)
        self.folders = Folders(ns_client)
        self.files = Files(ns_client)
        self.expense_categories = ExpenseCategory(ns_client)
        self.custom_lists = CustomLists(ns_client)
        self.custom_segments = CustomSegments(ns_client)
        self.custom_records = CustomRecords(ns_client)
        self.custom_record_types = CustomRecordTypes(ns_client)
        self.customers = Customers(ns_client)
        self.projects = Projects(ns_client)
        self.vendor_payments = VendorPayments(ns_client)
        self.invoices = Invoices(ns_client)
        self.terms = Terms(ns_client)
        self.tax_items = TaxItems(ns_client)
        self.tax_groups = TaxGroups(ns_client)
        self.credit_memos = CreditMemos(ns_client)
        self.usages = Usage(ns_client)
