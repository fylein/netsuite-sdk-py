import logging
from collections import OrderedDict

from netsuitesdk.internal.utils import PaginatedSearch
from .base import ApiBase

logger = logging.getLogger(__name__)


class VendorBills(ApiBase):
    """
    VendorBills are not directly searchable - only via as transactions
    """

    SIMPLE_FIELDS = [
        'memo',
        'tranDate',
        'tranId',
        'itemList',
        'customFieldList'
    ]

    RECORD_REF_FIELDS = [
        'currency',
        'class',
        'location',
        'department',
        'account',
        'entity',
        'subsidiary'
    ]

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

    def _build_vendor_bill(self, data) -> OrderedDict:
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

        self.build_simple_fields(self.SIMPLE_FIELDS, data, vb)
        self.build_record_ref_fields(self.RECORD_REF_FIELDS, data, vb)

        return vb

    def post(self, data) -> OrderedDict:
        vendor_bill = self._build_vendor_bill(data)

        logger.debug('able to create VendorBill = %s', vendor_bill)
        res = self.ns_client.upsert(vendor_bill)
        return self._serialize(res)

    def post_batch(self, records) -> [OrderedDict]:
        vendor_bills = [self._build_vendor_bill(record) for record in records]

        responses = self.ns_client.upsert_list(vendor_bills)
        return [self._serialize(response) for response in responses]
