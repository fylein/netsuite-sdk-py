from collections import OrderedDict

from .base import ApiBase
import logging

logger = logging.getLogger(__name__)


class Vendors(ApiBase):
    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='Vendor')

    def post(self, data) -> OrderedDict:
        assert data['externalId'], 'missing external id'
        vendor = self.ns_client.Vendor(externalId=data['externalId'])

        vendor['currency'] = self.ns_client.RecordRef(**(data['currency']))

        vendor['subsidiary'] = self.ns_client.RecordRef(**(data['subsidiary']))

        vendor['representingSubsidiary'] = self.ns_client.RecordRef(**(data['representingSubsidiary']))

        vendor['workCalendar'] = self.ns_client.RecordRef(**(data['workCalendar']))

        if 'entityId' in data:
            vendor['entityId'] = data['entityId']

        if 'isPerson' in data:
            vendor['isPerson'] = data['isPerson']

        if 'companyName' in data:
            vendor['companyName'] = data['companyName']

        if 'firstName' in data:
            vendor['firstName'] = data['firstName']

        if 'lastName' in data:
            vendor['lastName'] = data['lastName']

        if 'email' in data:
            vendor['email'] = data['email']

        logger.debug('able to create vendor = %s', vendor)
        res = self.ns_client.upsert(vendor)
        return self._serialize(res)
