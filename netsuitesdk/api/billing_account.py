from collections import OrderedDict

from .base import ApiBase
import logging

logger = logging.getLogger(__name__)


class BillingAccount(ApiBase):
    SIMPLE_FIELDS = [
        'createdBy',
        'createdDate',
        'customFieldList',
        'customerDefault',
        'frequency',
        'idNumber',
        'inactive',
        'lastBillCycleDate',
        'lastBillDate',
        'memo',
        'name',
        'nextBillCycleDate',
        'startDate',
        'nullFieldList',
    ]

    RECORD_REF_FIELDS = [
        'billingSchedule',
        'cashSaleForm',
        'class',
        'currency',
        'customForm',
        'customer',
        'department',
        'invoiceForm',
        'location',
        'subsidiary',
    ]

    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='BillingAccount')

    def post(self, data) -> OrderedDict:
        assert data['externalId'], 'missing external id'
        billing_account = self.ns_client.BillingAccount(**data)

        self.build_simple_fields(self.SIMPLE_FIELDS, data, billing_account)

        self.build_record_ref_fields(self.RECORD_REF_FIELDS, data, billing_account)

        logger.debug('able to create billing account = %s', billing_account)

        res = self.ns_client.upsert(billing_account)
        return self._serialize(res)
