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
        'ListOrRecordRef',
        'SearchColumnStringField',
        'SearchColumnSelectField',
        'SearchResult',
        'SearchEnumMultiSelectField',
        'SearchStringField',
        'SearchMultiSelectField',
        'SearchDateField',
        'SearchLongField',
        'Status',
        'StatusDetail',
        'TokenPassport',
        'TokenPassportSignature',
        'WsRole',
        'DateCustomFieldRef',
        'CustomFieldList',
        'DoubleCustomFieldRef',
        'StringCustomFieldRef',
        'CustomRecordRef',
        'SelectCustomFieldRef'
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
        'Address',
        'CustomerSearchBasic',
        'JobSearchBasic',
        'LocationSearchBasic',
        'TransactionSearchBasic',
        'VendorSearchBasic',
        'SubsidiarySearchBasic',
        'EmployeeSearchBasic',
        'FolderSearchBasic',
        'FileSearchBasic',
        'CustomRecordSearchBasic',
        'CustomListSearchBasic',
        'TermSearchBasic',
        'DepartmentSearchBasic',
        'ItemSearchBasic', 'ItemSearchRowBasic',
        'ClassificationSearchBasic',
    ],

    'ns6': [
      'ItemCostEstimateType',
    ],

    # urn:relationships.lists.webservices.netsuite.com
    'ns13': [
        'CustomerAddressbook', 'CustomerAddressbookList',
        'Customer', 'CustomerSearch',
        'Vendor', 'VendorSearch',
        'Job', 'JobSearch',
        'VendorAddressbook', 'VendorAddressbookList',
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
        'Term', 'TermSearch',
        'SalesTaxItem', 'SalesTaxItemSearch',
        'TaxGroup', 'TaxGroupSearch',
        'DepartmentSearch',
        'ItemSearch', 'ItemSearchAdvanced', 'ItemSearchRow',
        'ClassificationSearch',
    ],

    'ns19': [
        'Invoice',
        'InvoiceItem',
        'InvoiceItemList',
        'TransactionSearch',
        'TransactionSearchAdvanced',
    ],

    # urn:purchases_2017_2.transactions.webservices.netsuite.com
    # https://webservices.netsuite.com/xsd/transactions/v2017_2_0/purchases.xsd
    'ns21': [
        'VendorBill',
        'VendorBillExpense',
        'VendorBillExpenseList',
        'VendorBillItem',
        'VendorBillItemList',
        'VendorCredit',
        'VendorCreditApply',
        'VendorCreditApplyList',
        'VendorCreditExpense',
        'VendorCreditExpenseList',
        'VendorCreditItem',
        'VendorCreditItemList',
        'VendorPayment',
        'VendorPaymentApplyList',
        'VendorPaymentCredit',
        'VendorPaymentCreditList',
        'VendorPaymentApply'
    ],

    'ns23': [
        'CreditMemo',
        'CreditMemoApply',
        'CreditMemoApplyList',
        'CreditMemoItem',
        'CreditMemoItemList',
    ],

    # urn:general_2019_2.transactions.webservices.netsuite.com
    # https://webservices.netsuite.com/xsd/transactions/v2019_2_0/general.xsd
    'ns31': [
        'JournalEntry',
        'JournalEntryLine',
        'JournalEntryLineList',
    ],

    'ns32': [
        'CustomRecord',
        'CustomRecordCustomField',
        'CustomRecordSearch',
        'CustomListSearch',
        'CustomRecordType'
    ],

    # https://webservices.netsuite.com/xsd/lists/v2019_2_0/employees.xsd
    'ns34': [
        'EmployeeSearch',
        'Employee'
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
        'SearchEnumMultiSelectFieldOperator',
        'SearchStringFieldOperator',
        'SearchDateFieldOperator',
        'SearchLongFieldOperator',
    ],
}
