from collections import OrderedDict

from .base import ApiBase
import logging

logger = logging.getLogger(__name__)

class Customers(ApiBase):
    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='Customer')

    def post(self, data) -> OrderedDict:
        assert data['externalId'], 'missing external id'
        customer = self.ns_client.Customer(externalId=data['externalId'])

        customer['currency'] = self.ns_client.RecordRef(**(data['currency']))

        customer['subsidiary'] = self.ns_client.RecordRef(**(data['subsidiary']))

        customer['representingSubsidiary'] = self.ns_client.RecordRef(**(data['representingSubsidiary']))

        customer['monthlyClosing'] = self.ns_client.RecordRef(**(data['monthlyClosing']))

        if 'entityId' in data:
            customer['entityId'] = data['entityId']

        if 'isPerson' in data:
            customer['isPerson'] = data['isPerson']

        if 'companyName' in data:
            customer['companyName'] = data['companyName']

        if 'firstName' in data:
            customer['firstName'] = data['firstName']

        if 'lastName' in data:
            customer['lastName'] = data['lastName']

        if 'email' in data:
            customer['email'] = data['email']

        if 'addressbookList' in data:
            customer['addressbookList'] = data['addressbookList']

        logger.debug('able to create customer = %s', customer)
        res = self.ns_client.upsert(customer)
        return self._serialize(res)
