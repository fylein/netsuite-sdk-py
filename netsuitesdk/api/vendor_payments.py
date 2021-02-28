import logging

from netsuitesdk.internal.utils import PaginatedSearch

from .base import ApiBase
from collections import OrderedDict

logger = logging.getLogger(__name__)


class VendorPayments(ApiBase):
    """
    VendorPayments are not directly searchable - only via as transactions
    """

    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='vendorPayment')

    def get_all_generator(self):
        record_type_search_field = self.ns_client.SearchStringField(searchValue='VendorPayment', operator='contains')
        basic_search = self.ns_client.basic_search_factory('Transaction', recordType=record_type_search_field)
        paginated_search = PaginatedSearch(client=self.ns_client,
                                           type_name='Transaction',
                                           basic_search=basic_search,
                                           pageSize=20)
        return self._paginated_search_to_generator(paginated_search=paginated_search)

    def post(self, data) -> OrderedDict:
        assert data['externalId'], 'missing external id'
        vp = self.ns_client.VendorPayment(externalId=data['externalId'])
        apply_lists = []
        for eod in data['applyList']['apply']:
            vpal = self.ns_client.VendorPaymentApply(**eod)
            apply_lists.append(vpal)

        vp['applyList'] = self.ns_client.VendorPaymentApplyList(apply=apply_lists)

        vp['currency'] = self.ns_client.RecordRef(**(data['currency']))

        if 'amount' in data:
            vp['amount'] = data['amount']

        if 'memo' in data:
            vp['memo'] = data['memo']

        if 'tranDate' in data:
            vp['tranDate'] = data['tranDate']

        if 'tranId' in data:
            vp['tranId'] = data['tranId']

        if 'class' in data:
            vp['class'] = self.ns_client.RecordRef(**(data['class']))

        if 'apAcct' in data:
            vp['apAcct'] = self.ns_client.RecordRef(**(data['apAcct']))

        if 'location' in data:
            vp['location'] = self.ns_client.RecordRef(**(data['location']))

        if 'department' in data:
            vp['department'] = self.ns_client.RecordRef(**(data['department']))

        if 'account' in data:
            vp['account'] = self.ns_client.RecordRef(**(data['account']))

        if 'externalId' in data:
            vp['externalId'] = data['externalId']

        vp['entity'] = self.ns_client.RecordRef(**(data['entity']))
        logger.debug('able to create vp = %s', vp)
        res = self.ns_client.upsert(vp)
        return self._serialize(res)
