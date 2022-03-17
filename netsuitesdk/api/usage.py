from collections import OrderedDict

from .base import ApiBase
import logging

logger = logging.getLogger(__name__)


class Usage(ApiBase):
    SIMPLE_FIELDS = [
        'memo',
        'usageDate',
        'usageQuantity',
        'nullFieldList',
    ]

    RECORD_REF_FIELDS = [
        'customForm',
        'customer',
        'item',
        'subscriptionPlan',
        'usageSubscription',
        'usageSubscriptionLine',
    ]

    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='Usage')

    def post(self, data) -> OrderedDict:
        assert data['externalId'], 'missing external id'
        usage = self.ns_client.Usage(**data)

        self.build_simple_fields(self.SIMPLE_FIELDS, data, usage)

        self.build_record_ref_fields(self.RECORD_REF_FIELDS, data, usage)

        logger.debug('able to create usage = %s', usage)

        res = self.ns_client.upsert(usage)
        return self._serialize(res)
