import logging

from netsuitesdk.internal.utils import PaginatedSearch

from .base import ApiBase
from typing import List
from collections import OrderedDict

logger = logging.getLogger(__name__)


class VendorBills(ApiBase):
    """
    VendorBills are not directly searchable - only via as transactions
    """

    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='vendorBill')

    def get_all_generator(self):
        record_type_search_field = self.ns_client.SearchStringField(searchValue='VendorBill', operator='contains')
        basic_search = self.ns_client.basic_search_factory('Transaction', recordType=record_type_search_field)
        paginated_search = PaginatedSearch(client=self.ns_client,
                                           type_name='Transaction',
                                           basic_search=basic_search,
                                           pageSize=20)
        return self._paginated_search_to_generator(paginated_search=paginated_search)

    def post(self, data) -> OrderedDict:
        assert data['externalId'], 'missing external id'
        vb = self.ns_client.VendorBill(externalId=data['externalId'])
        expense_list = []
        for eod in data['expenseList']:
            if 'customFieldList' in eod and eod['customFieldList']:
                custom_fields = []
                for field in eod['customFieldList']:
                    if field['type'] == 'String':
                        custom_fields.append(
                            self.ns_client.StringCustomFieldRef(
                                scriptId=field['scriptId'] if 'scriptId' in field else None,
                                internalId=field['internalId'] if 'internalId' in field else None,
                                value=field['value']
                            )
                        )
                    elif field['type'] == 'Select':
                        custom_fields.append(
                            self.ns_client.SelectCustomFieldRef(
                                scriptId=field['scriptId'] if 'scriptId' in field else None,
                                internalId=field['internalId'] if 'internalId' in field else None,
                                value=self.ns_client.ListOrRecordRef(
                                    internalId=field['value']
                                )
                            )
                        )
                eod['customFieldList'] = self.ns_client.CustomFieldList(custom_fields)
            vbe = self.ns_client.VendorBillExpense(**eod)
            expense_list.append(vbe)
        
        vb['expenseList'] = self.ns_client.VendorBillExpenseList(expense=expense_list)
        vb['currency'] = self.ns_client.RecordRef(**(data['currency']))

        if 'memo' in data:
            vb['memo'] = data['memo']

        if 'tranDate' in data:
            vb['tranDate'] = data['tranDate']

        if 'tranId' in data:
            vb['tranId'] = data['tranId']

        if 'class' in data:
            vb['class'] = self.ns_client.RecordRef(**(data['class']))

        if 'location' in data:
            vb['location'] = self.ns_client.RecordRef(**(data['location']))

        if 'department' in data:
            vb['department'] = self.ns_client.RecordRef(**(data['department']))

        if 'account' in data:
            vb['account'] = self.ns_client.RecordRef(**(data['account']))

        vb['entity'] = self.ns_client.RecordRef(**(data['entity']))
        logger.debug('able to create vb = %s', vb)
        res = self.ns_client.upsert(vb)
        return self._serialize(res)
