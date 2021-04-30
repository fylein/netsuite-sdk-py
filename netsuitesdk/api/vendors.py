from collections import OrderedDict

from .base import ApiBase
import logging

logger = logging.getLogger(__name__)


class Vendors(ApiBase):
    SIMPLE_FIELDS = [
        'accountNumber',
        'addressbookList',
        'altEmail',
        'altName',
        'altPhone',
        'balance',
        'balancePrimary',
        'bcn',
        'billPay',
        'comments',
        'companyName',
        'creditLimit',
        'currencyList',
        'customFieldList',
        'dateCreated',
        'defaultAddress',
        'eligibleForCommission',
        'email',
        'emailPreference',
        'emailTransactions',
        'entityId',
        'fax',
        'faxTransactions',
        'firstName',
        'giveAccess',
        'globalSubscriptionStatus',
        'homePhone',
        'internalId',
        'is1099Eligible',
        'isAccountant',
        'isInactive',
        'isJobResourceVend',
        'isPerson',
        'laborCost',
        'lastModifiedDate',
        'lastName',
        'legalName',
        'middleName',
        'mobilePhone',
        'openingBalance',
        'openingBalanceDate',
        'password',
        'password2',
        'phone',
        'phoneticName',
        'predConfidence',
        'predictedDays',
        'pricingScheduleList',
        'printOnCheckAs',
        'printTransactions',
        'purchaseOrderAmount',
        'purchaseOrderQuantity',
        'purchaseOrderQuantityDiff',
        'receiptAmount',
        'receiptQuantity',
        'receiptQuantityDiff',
        'requirePwdChange',
        'rolesList',
        'salutation',
        'sendEmail',
        'subscriptionsList',
        'taxIdNum',
        'taxRegistrationList',
        'title',
        'unbilledOrders',
        'unbilledOrdersPrimary',
        'url',
        'vatRegNumber',
        'nullFieldList',
    ]

    RECORD_REF_FIELDS = [
        'category',
        'customForm',
        'defaultTaxReg',
        'expenseAccount',
        'image',
        'incoterm',
        'openingBalanceAccount',
        'payablesAccount',
        'taxItem',
        'terms',
    ]

    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='Vendor')

    def post(self, data) -> OrderedDict:
        assert data['externalId'], 'missing external id'
        vendor = self.ns_client.Vendor(externalId=data['externalId'])

        vendor['currency'] = self.ns_client.RecordRef(**(data['currency']))

        vendor['subsidiary'] = self.ns_client.RecordRef(**(data['subsidiary']))

        vendor['representingSubsidiary'] = self.ns_client.RecordRef(**(data['representingSubsidiary']))

        vendor['workCalendar'] = self.ns_client.RecordRef(**(data['workCalendar']))

        self.build_simple_fields(self.SIMPLE_FIELDS, data, vendor)

        self.build_record_ref_fields(self.RECORD_REF_FIELDS, data, vendor)

        logger.debug('able to create vendor = %s', vendor)
        res = self.ns_client.upsert(vendor)
        return self._serialize(res)
