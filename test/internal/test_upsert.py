from netsuitesdk.internal.utils import PaginatedSearch
import logging
import pytest
import zeep

logger = logging.getLogger(__name__)

#@pytest.mark.parametrize('type_name', ['Account', 'Vendor', 'Department', 'Location', 'Classification'])
def get_record(ns, type_name):
    paginated_search = PaginatedSearch(client=ns, type_name=type_name, pageSize=20)
    return paginated_search.records[0]

def get_location(ns):
    return get_record(ns, 'Location')

def get_department(ns):
    return get_record(ns, 'Department')

def get_class(ns):
    return get_record(ns, 'Classification')

def get_vendor(ns):
    return get_record(ns, 'Vendor')

def get_category_account(ns):
    return ns.get(recordType='account', internalId=84)

def get_currency(ns):
    return ns.get(recordType='currency', internalId='1')

def get_employee(ns):
    return ns.get(recordType='employee', internalId='1648')

def test_upsert_vendor_bill(ns):
    vendor_ref = ns.RecordRef(type='vendor', internalId=get_vendor(ns).internalId)
    bill_account_ref = ns.RecordRef(type='account', internalId=25)
    cat_account_ref = ns.RecordRef(type='account', internalId=get_category_account(ns).internalId)
    loc_ref = ns.RecordRef(type='location', internalId=get_location(ns).internalId)
    dep_ref = ns.RecordRef(type='department', internalId=get_department(ns).internalId)
    class_ref = ns.RecordRef(type='classification', internalId=get_department(ns).internalId)
    expenses = []

    vbe1 = ns.VendorBillExpense()
    vbe1['account'] = cat_account_ref
    vbe1['amount'] = 10.0
    vbe1['department'] = dep_ref
    vbe1['class'] = class_ref
    vbe1['location'] = loc_ref

    expenses.append(vbe1)
    vbe1 = ns.VendorBillExpense()
    vbe1['account'] = cat_account_ref
    vbe1['amount'] = 20.0
    vbe1['department'] = dep_ref
    vbe1['class'] = class_ref
    vbe1['location'] = loc_ref

    expenses.append(vbe1)

    bill = ns.VendorBill(externalId='1234')
    bill['currency'] = ns.RecordRef(type='currency', internalId=get_currency(ns).internalId) # US dollar
    bill['exchangerate'] = 1.0
    bill['expenseList'] = ns.VendorBillExpenseList(expense=expenses)
    bill['memo'] = 'test memo'
    bill['class'] = class_ref
    bill['location'] = loc_ref
    bill['entity'] = vendor_ref
    logger.debug('upserting bill %s', bill)
    record_ref = ns.upsert(bill)
    logger.debug('record_ref = %s', record_ref)
    assert record_ref['externalId'] == '1234', 'External ID does not match'

    bill2 = ns.get(recordType='vendorBill', externalId='1234')
    logger.debug('bill2 = %s', str(bill2))
    assert (29.99 < bill2['userTotal']) and (bill2['userTotal'] < 30.01), 'Bill total is not 30.0'

def test_upsert_journal_entry(ns):
    vendor_ref = ns.RecordRef(type='vendor', internalId=get_vendor(ns).internalId)
    cat_account_ref = ns.RecordRef(type='account', internalId=get_category_account(ns).internalId)
    loc_ref = ns.RecordRef(type='location', internalId=get_location(ns).internalId)
    dep_ref = ns.RecordRef(type='department', internalId=get_department(ns).internalId)
    class_ref = ns.RecordRef(type='classification', internalId=get_department(ns).internalId)
    lines = []

    credit_line = ns.JournalEntryLine()
    credit_line['account'] = cat_account_ref
    credit_line['department'] = dep_ref
    credit_line['class'] = class_ref
    credit_line['location'] = loc_ref
    credit_line['entity'] = vendor_ref
    credit_line['credit'] = 20.0

    lines.append(credit_line)

    debit_line = ns.JournalEntryLine()
    debit_line['account'] = cat_account_ref
    debit_line['department'] = dep_ref
    debit_line['class'] = class_ref
    debit_line['location'] = loc_ref
    debit_line['entity'] = vendor_ref
    debit_line['debit'] = 20.0

    lines.append(debit_line)

    journal_entry = ns.JournalEntry(externalId='JE_1234')
    journal_entry['currency'] = ns.RecordRef(type='currency', internalId=get_currency(ns).internalId)  # US dollar
    journal_entry['subsidiary'] = ns.RecordRef(type='subsidiary', internalId='1')
    journal_entry['exchangerate'] = 1.0
    journal_entry['lineList'] = ns.JournalEntryLineList(line=lines)
    journal_entry['memo'] = 'test memo'
    logger.debug('upserting journal entry %s', journal_entry)
    record_ref = ns.upsert(journal_entry)
    logger.debug('record_ref = %s', record_ref)
    assert record_ref['externalId'] == 'JE_1234', 'External ID does not match'

    je = ns.get(recordType='journalEntry', externalId='JE_1234')
    logger.debug('je = %s', str(je))
    assert (je['externalId'] == 'JE_1234'), 'Journal Entry External ID does not match'


def test_upsert_expense_report(ns):
    employee_ref = ns.RecordRef(type='employee', internalId=get_employee(ns).internalId)
    bill_account_ref = ns.RecordRef(type='account', internalId=25)
    cat_account_ref = ns.RecordRef(type='account', internalId='1')
    loc_ref = ns.RecordRef(type='location', internalId=get_location(ns).internalId)
    dep_ref = ns.RecordRef(type='department', internalId=get_department(ns).internalId)
    class_ref = ns.RecordRef(type='classification', internalId=get_department(ns).internalId)
    currency_ref = ns.RecordRef(type='currency', internalId=get_currency(ns).internalId)
    expenses = []

    er = ns.ExpenseReportExpense()
    er['category'] = cat_account_ref
    er['amount'] = 10.0
    er['department'] = dep_ref
    er['class'] = class_ref
    er['location'] = loc_ref
    er['currency'] = currency_ref

    expenses.append(er)

    expense_report = ns.ExpenseReport(externalId='EXPR_1')
    expense_report['expenseReportCurrency'] = currency_ref  # US dollar
    expense_report['exchangerate'] = 1.0
    expense_report['expenseList'] = ns.ExpenseReportExpenseList(expense=expenses)
    expense_report['memo'] = 'test memo'
    expense_report['entity'] = employee_ref
    logger.debug('upserting expense report %s', expense_report)
    record_ref = ns.upsert(expense_report)
    logger.debug('record_ref = %s', record_ref)
    assert record_ref['externalId'] == 'EXPR_1', 'External ID does not match'

    expr = ns.get(recordType='ExpenseReport', externalId='EXPR_1')
    logger.debug('expense report = %s', str(expr))
