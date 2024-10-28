#add the file to pod before running this script
# kube_prod_integrations_us cp /Users/ruuushhh/workspace/netsuite-sdk-py/gxc_update_batch_1_50.csv integrations/netsuite-api-5b4f8d84d5-s57q2:gxc_update_batch_1_50.csv


import json
from apps.workspaces.models import NetSuiteCredentials
from apps.netsuite.models import CreditCardCharge, CreditCardChargeLineItem
from apps.fyle.models import Expense, ExpenseGroup
from typing import Dict
from requests_oauthlib import OAuth1Session
import csv
from datetime import datetime
from apps.workspaces.models import FyleCredential, Workspace
from typing import List
from django.conf import settings
from fyle_accounting_mappings.models import DestinationAttribute

workspace_id=439
netsuite_credentials = NetSuiteCredentials.objects.get(workspace_id=workspace_id)
failed_records = []

def construct_credit_card_charge_lineitems(
        credit_card_charge_lineitem: CreditCardChargeLineItem,
        attachment_links: Dict, cluster_domain: str, org_id: str) -> List[Dict]:
    line = credit_card_charge_lineitem
    lines = []
    expense = Expense.objects.get(pk=line.expense_id)
    netsuite_custom_segments = line.netsuite_custom_segments
    if attachment_links and expense.expense_id in attachment_links:
        netsuite_custom_segments.append(
            {
                'scriptId': 'custcolfyle_receipt_link',
                'value': attachment_links[expense.expense_id]
            }
        )
        netsuite_custom_segments.append(
            {
                'scriptId': 'custcolfyle_receipt_link_2',
                'type': 'String',
                'value': attachment_links[expense.expense_id]
            }
        )
    netsuite_custom_segments.append(
        {
            'scriptId': 'custcolfyle_expense_url',
            'value': '{}/app/admin/#/enterprise/view_expense/{}?org_id={}'.format(
                settings.FYLE_EXPENSE_URL,
                expense.expense_id,
                org_id
            )
        }
    )
    netsuite_custom_segments.append(
        {
            'scriptId': 'custcolfyle_expense_url_2',
            'value': '{}/app/admin/#/enterprise/view_expense/{}?org_id={}'.format(
                settings.FYLE_EXPENSE_URL,
                expense.expense_id,
                org_id
            )
        }
    )
    line = {
        'account': {
            'internalId': line.account_id
        },
        'amount': line.amount - line.tax_amount if (line.tax_item_id and line.tax_amount is not None) else line.amount,
        'memo': line.memo,
        'grossAmt': line.amount,
        'department': {
            'internalId': line.department_id
        },
        'class': {
            'internalId': line.class_id
        },
        'location': {
            'internalId': line.location_id
        },
        'customer': {
            'internalId': line.customer_id
        },
        'customFieldList': netsuite_custom_segments,
        'isBillable': line.billable,
        'taxAmount': None,
        'taxCode': {
            'name': None,
            'internalId': line.tax_item_id if (line.tax_item_id and line.tax_amount is not None) else None,
            'externalId': None,
            'type': 'taxGroup'
        },
    }
    lines.append(line)
    return lines

from datetime import datetime
def construct_credit_card_charge(
        credit_card_charge: CreditCardCharge,
        credit_card_charge_lineitem: CreditCardChargeLineItem, attachment_links: Dict, transaction_date) -> Dict:
    fyle_credentials = FyleCredential.objects.get(workspace_id=credit_card_charge.expense_group.workspace_id)
    cluster_domain = fyle_credentials.cluster_domain
    org_id = Workspace.objects.get(id=credit_card_charge.expense_group.workspace_id).fyle_org_id
    if transaction_date:
        transaction_date = transaction_date
    else:
        transaction_date = credit_card_charge.transaction_date
        transaction_date = transaction_date.strftime('%m/%d/%Y')
    credit_card_charge_payload = {
        'account': {
            'internalId': credit_card_charge.credit_card_account_id
        },
        'entity': {
            'internalId': credit_card_charge.entity_id
        },
        'subsidiary': {
            'internalId': credit_card_charge.subsidiary_id
        },
        'location': {
            'internalId': credit_card_charge.location_id
        },
        'currency': {
            'internalId': credit_card_charge.currency
        },
        'department': {
            'internalId': credit_card_charge.department_id
        },
        'class': {
            'internalId': credit_card_charge.class_id
        },
        'tranDate': transaction_date,
        'memo': credit_card_charge.memo,
        'tranid': credit_card_charge.reference_number,
        'expenses': construct_credit_card_charge_lineitems(
            credit_card_charge_lineitem, attachment_links, cluster_domain, org_id
        ),
        'externalId': credit_card_charge.external_id
    }
    return credit_card_charge_payload

def post_credit_card_charge(credit_card_charge: CreditCardCharge,
                                credit_card_charge_lineitem: CreditCardChargeLineItem, attachment_links: Dict,
                                refund: bool, netsuite_credentials, transaction_date=None):
    """
    Post vendor credit_card_charges to NetSuite
    """
    account = netsuite_credentials.ns_account_id.replace('_', '-')
    consumer_key = netsuite_credentials.ns_consumer_key
    consumer_secret = netsuite_credentials.ns_consumer_secret
    token_key = netsuite_credentials.ns_token_id
    token_secret = netsuite_credentials.ns_token_secret
    is_sandbox = False
    if '-SB' in account:
        is_sandbox = True
    url = f"https://{account.lower()}.restlets.api.netsuite.com/app/site/hosting/restlet.nl?" \
            f"script=customscript_cc_charge_fyle&deploy=customdeploy_cc_charge_fyle"
    if refund:
        credit_card_charge_lineitem.amount = abs(credit_card_charge_lineitem.amount)
        url = f"https://{account.lower()}.restlets.api.netsuite.com/app/site/hosting/restlet.nl?" \
                f"script=customscript_cc_refund_fyle&deploy=customdeploy_cc_refund_fyle"
    credit_card_charges_payload = construct_credit_card_charge(
        credit_card_charge, credit_card_charge_lineitem, attachment_links, transaction_date)
    credit_card_charges_payload['internalId'] = credit_card_charge.expense_group.response_logs['internalId']  
    oauth = OAuth1Session(
        client_key=consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=token_key,
        resource_owner_secret=token_secret,
        realm=netsuite_credentials.ns_account_id.upper() if is_sandbox else account,
        signature_method='HMAC-SHA256'
    )
    raw_response = oauth.put(
        url, headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }, data=json.dumps(credit_card_charges_payload))
    status_code = raw_response.status_code
    if status_code == 200 and 'success' in json.loads(raw_response.text) and json.loads(raw_response.text)['success']:
        print(json.loads(raw_response.text))
    else:
        failed_records.append({credit_card_charge.expense_group.response_logs['internalId']: json.loads(raw_response.text)})
        print(failed_records)

file_path = 'gxc_update_batch_1_50.csv'
with open(file_path, mode='r') as file:
    reader = csv.DictReader(file)
    for r in reader:
        expense: Expense = Expense.objects.get(expense_number=r['expense_number'], workspace_id=workspace_id)
        expense_group = ExpenseGroup.objects.get(expenses=expense, workspace_id=workspace_id)
        credit_card_charge = CreditCardCharge.objects.get(expense_group=expense_group)
        credit_card_charge_lineitems = CreditCardChargeLineItem.objects.get(credit_card_charge=credit_card_charge)
        refund = False
        transaction_date = None
        if expense.amount < 0:
            refund = True
        credit_card_account_id = None
        attachment_links = {}
        attachment_links[expense.expense_id] = r['receipt_url']
        credit_card_charge_lineitems.amount = r['netsuite_amount'] if r['netsuite_amount'] != "" else credit_card_charge_lineitems.amount
        if r['netsuite_date'] != "":
            transaction_date = r['netsuite_date']
        if r['netsuite_account'] != "":
            credit_card_account_id = DestinationAttribute.objects.filter(workspace_id=workspace_id, attribute_type='CREDIT_CARD_ACCOUNT', value=r['netsuite_account']).first()
            credit_card_charge.credit_card_account_id = credit_card_account_id.destination_id if credit_card_account_id else credit_card_charge.credit_card_account_id
        credit_card_charge.netsuite_receipt_url = r['receipt_url']
        credit_card_charge.save()
        credit_card_charge_lineitems.save()
        post_credit_card_charge(credit_card_charge, credit_card_charge_lineitems, attachment_links, refund, netsuite_credentials, transaction_date)

print("Final Failed records", failed_records)


# CSV generate query
#  \copy (select une.internalid, une.expense_number, une.fyle_amount, une.netsuite_amount, une.fyle_account, une.fyle_account_name, une.netsuite_account, une.fyle_date, une.netsuite_date, une.receipt_url, e.accounting_export_summary->>'url' as export_url from update_netsuite_expenses une join expenses e on une.expense_number=e.expense_number where e.workspace_id=439) to '/Users/ruuushhh/Downloads/gxc_update_batch_1_50.csv' with csv header;