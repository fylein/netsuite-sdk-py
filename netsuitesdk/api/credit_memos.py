from collections import OrderedDict

from .base import ApiBase
import logging

logger = logging.getLogger(__name__)


class CreditMemos(ApiBase):
    SIMPLE_FIELDS = [
        'accountingBookDetailList',
        'altHandlingCost',
        'altShippingCost',
        'amountPaid',
        'amountRemaining',
        'applied',
        'applyList',
        'autoApply',
        'balance',
        'billingAddress',
        'contribPct',
        'createdDate',
        'currencyName',
        'customFieldList',
        'deferredRevenue',
        'discountRate',
        'discountTotal',
        'email',
        'estGrossProfit',
        'estGrossProfitPercent',
        'exchangeRate',
        'excludeCommission',
        'fax',
        'giftCertApplied',
        'giftCertAvailable',
        'giftCertTotal',
        'handlingCost',
        'handlingTax1Rate',
        'handlingTax2Rate',
        'internalId',
        'isMultiShipTo',
        'isTaxable',
        'itemList',
        'lastModifiedDate',
        'memo',
        'message',
        'onCreditHold',
        'otherRefNum',
        'partnersList',
        'recognizedRevenue',
        'revRecOnRevCommitment',
        'revenueStatus',
        'salesEffectiveDate',
        'salesTeamList',
        'shippingCost',
        'shippingTax1Rate',
        'shippingTax2Rate',
        'source',
        'status',
        'subTotal',
        'syncPartnerTeams',
        'syncSalesTeams',
        'tax2Total',
        'taxDetailsList',
        'taxDetailsOverride',
        'taxPointDate',
        'taxRate',
        'taxRegOverride',
        'taxTotal',
        'toBeEmailed',
        'toBeFaxed',
        'toBePrinted',
        'total',
        'totalCostEstimate',
        'tranDate',
        'tranId',
        'tranIsVsoeBundle',
        'unapplied',
        'vatRegNum',
        'vsoeAutoCalc',
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
        'discountItem',
        'entityTaxRegNum',
        'giftCert',
        'handlingTaxCode',
        'job',
        'leadSource',
        'location',
        'messageSel',
        'nexus',
        'partner',
        'postingPeriod',
        'promoCode',
        'salesGroup',
        'salesRep',
        'shipMethod',
        'shippingTaxCode',
        'subsidiary',
        'subsidiaryTaxRegNum',
        'taxItem',
    ]

    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='CreditMemo')

    def post(self, data) -> OrderedDict:
        assert data['externalId'], 'missing external id'
        credit_memo = self.ns_client.CreditMemo(**data)

        credit_memo['entity'] = self.ns_client.RecordRef(**(data['entity']))

        self.build_simple_fields(self.SIMPLE_FIELDS, data, credit_memo)

        self.build_record_ref_fields(self.RECORD_REF_FIELDS, data, credit_memo)

        logger.debug('able to create credit memo = %s', credit_memo)

        res = self.ns_client.upsert(credit_memo)
        return self._serialize(res)
