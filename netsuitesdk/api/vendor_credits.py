from collections import OrderedDict

from .base import ApiBase
import logging

logger = logging.getLogger(__name__)


class VendorCredits(ApiBase):
    SIMPLE_FIELDS = [
        'accountingBookDetailList',
        'applied',
        'applyList',
        'autoApply',
        'billingAddress',
        'createdDate',
        'currencyName',
        'customFieldList',
        'exchangeRate',
        'expenseList',
        'internalId',
        'itemList',
        'lastModifiedDate',
        'memo',
        'taxDetailsList',
        'taxDetailsOverride',
        'taxPointDate',
        'taxRegOverride',
        'total',
        'tranDate',
        'tranId',
        'transactionNumber',
        'unApplied',
        'userTaxTotal',
        'userTotal',
        'nullFieldList',
    ]

    RECORD_REF_FIELDS = [
        'account',
        'billAddressList',
        'class',
        'createdFrom',
        'currency',
        'customForm',
        'department',
        'entityTaxRegNum',
        'location',
        'nexus',
        'postingPeriod',
        'subsidiary',
        'subsidiaryTaxRegNum',
    ]

    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='VendorCredit')

    def post(self, data) -> OrderedDict:
        assert data['externalId'], 'missing external id'
        vendor_credit = self.ns_client.VendorCredit(**data)

        vendor_credit['entity'] = self.ns_client.RecordRef(**(data['entity']))

        self.build_simple_fields(self.SIMPLE_FIELDS, data, vendor_credit)

        self.build_record_ref_fields(self.RECORD_REF_FIELDS, data, vendor_credit)

        logger.debug('able to create vendor credit = %s', vendor_credit)

        res = self.ns_client.upsert(vendor_credit)
        return self._serialize(res)
