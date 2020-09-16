"""
Declares all NetSuite types which are available through attribute lookup `ns.<type>`
of a :class:`~netsuitesdk.client.NetSuiteClient` instance `ns`.
"""

COMPLEX_TYPES = {
    'ns0': [
        'BaseRef',
        'GetAllRecord',
        'GetAllResult',
        'Passport',
        'RecordList',
        'RecordRef',
        'SearchResult',
        'SearchStringField',
        'SearchMultiSelectField',
        'Status',
        'StatusDetail',
        'TokenPassport',
        'TokenPassportSignature',
        'WsRole',
        'CustomFieldList',
        'StringCustomFieldRef'
    ],

    # ns4: https://webservices.netsuite.com/xsd/platform/v2017_2_0/messages.xsd
    'ns4': [
        'ApplicationInfo',
        'GetAllRequest',
        'GetRequest',
        'GetResponse',
        'GetAllResponse',
        'PartnerInfo',
        'ReadResponse',
        'SearchPreferences',
        'SearchResponse'
    ],

    # https://webservices.netsuite.com/xsd/platform/v2017_2_0/common.xsd
    'ns5': [
        'AccountSearchBasic',
        'CustomerSearchBasic',
        'LocationSearchBasic',
        'TransactionSearchBasic',
        'VendorSearchBasic',
        'SubsidiarySearchBasic',
        'EmployeeSearchBasic',
        'FolderSearchBasic',
        'FileSearchBasic'
    ],

    # urn:relationships.lists.webservices.netsuite.com
    'ns13': [
        'Customer', 'CustomerSearch',
        'Vendor', 'VendorSearch',
    ],

    # urn:accounting_2017_2.lists.webservices.netsuite.com
    # https://webservices.netsuite.com/xsd/lists/v2017_2_0/accounting.xsd
    'ns17': [
        'Account', 'AccountSearch',
        'ExpenseCategory', 'ExpenseCategorySearch',
        'AccountingPeriod',
        'Classification', 'ClassificationSearch',
        'Department', 'DepartmentSearch',
        'Location', 'LocationSearch',
        'Subsidiary', 'SubsidiarySearch',
        'VendorCategory', 'VendorCategorySearch',
    ],

    'ns19': [
        'TransactionSearch',
    ],

    # urn:purchases_2017_2.transactions.webservices.netsuite.com
    # https://webservices.netsuite.com/xsd/transactions/v2017_2_0/purchases.xsd
    'ns21': [
        'VendorBill',
        'VendorBillExpense',
        'VendorBillExpenseList',
        'VendorBillItem',
        'VendorBillItemList',
        'VendorPayment',
    ],

    # urn:general_2019_2.transactions.webservices.netsuite.com
    # https://webservices.netsuite.com/xsd/transactions/v2019_2_0/general.xsd
    'ns31': [
        'JournalEntry',
        'JournalEntryLine',
        'JournalEntryLineList',
    ],

    # https://webservices.netsuite.com/xsd/lists/v2019_2_0/employees.xsd
    'ns34': [
        'EmployeeSearch',
    ],

    # urn:employees_2019_2.transactions.webservices.netsuite.com
    # https://webservices.netsuite.com/xsd/transactions/v2019_2_0/employees.xsd
    'ns38': [
        'ExpenseReport',
        'ExpenseReportExpense',
        'ExpenseReportExpenseList',
    ],
    'ns11': [
        'FolderSearch',
        'Folder',
        'File',
        'FileSearch'
    ],
}

SIMPLE_TYPES = {
    # ns1: view-source:https://webservices.netsuite.com/xsd/platform/v2017_2_0/coreTypes.xsd
    'ns1': [
        'RecordType',
        'GetAllRecordType',
        'SearchRecordType',
        'SearchStringFieldOperator',
    ],
}
