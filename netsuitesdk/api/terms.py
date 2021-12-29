from collections import OrderedDict

from .base import ApiBase
import logging

logger = logging.getLogger(__name__)

class Terms(ApiBase):
    SIMPLE_FIELDS = [
        'dateDriven',
        'dayDiscountExpires',
        'dayOfMonthNetDue',
        'daysUntilExpiry',
        'daysUntilNetDue',
        'discountPercent',
        'discountPercentDateDriven',
        'dueNextMonthIfWithinDays',
        'externalId',
        'installment',
        'internalId',
        'isInactive',
        'percentagesList',
        'preferred',
        'recurrenceCount',
        'recurrenceFrequency',
        'repeatEvery',
        'splitEvenly',
        'nullFieldList',
    ]

    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='Term')

    def post(self, data) -> OrderedDict:
        term = self.ns_client.Term(daysUntilNetDue=data['daysUntilNetDue'], name=data['name'])

        self.build_simple_fields(self.SIMPLE_FIELDS, data, term)

        logger.debug('able to create term = %s', term)
        res = self.ns_client.request('add', record=term)
        return self._serialize(res)
