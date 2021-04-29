from collections import OrderedDict

from .base import ApiBase
import logging

logger = logging.getLogger(__name__)

class Customers(ApiBase):
    SIMPLE_FIELDS = [
        'accountNumber',
        'addressbookList',
        'aging',
        'aging1',
        'aging2',
        'aging3',
        'aging4',
        'alcoholRecipientType',
        'altEmail',
        'altName',
        'altPhone',
        'balance',
        'billPay',
        'clickStream',
        'comments',
        'companyName',
        'consolAging',
        'consolAging1',
        'consolAging2',
        'consolAging3',
        'consolAging4',
        'consolBalance',
        'consolDaysOverdue',
        'consolDepositBalance',
        'consolOverdueBalance',
        'consolUnbilledOrders',
        'contactRolesList',
        'contribPct',
        'creditCardsList',
        'creditHoldOverride',
        'creditLimit',
        'currencyList',
        'customFieldList',
        'dateCreated',
        'daysOverdue',
        'defaultAddress',
        'defaultOrderPriority',
        'depositBalance',
        'displaySymbol',
        'downloadList',
        'email',
        'emailPreference',
        'emailTransactions',
        'endDate',
        'entityId',
        'estimatedBudget',
        'externalId',
        'fax',
        'faxTransactions',
        'firstName',
        'firstVisit',
        'giveAccess',
        'globalSubscriptionStatus',
        'groupPricingList',
        'homePhone',
        'internalId',
        'isBudgetApproved',
        'isInactive',
        'isPerson',
        'itemPricingList',
        'keywords',
        'language',
        'lastModifiedDate',
        'lastName',
        'lastPageVisited',
        'lastVisit',
        'middleName',
        'mobilePhone',
        'negativeNumberFormat',
        'numberFormat',
        'openingBalance',
        'openingBalanceDate',
        'overdueBalance',
        'overrideCurrencyFormat',
        'partnersList',
        'password',
        'password2',
        'phone',
        'phoneticName',
        'printOnCheckAs',
        'printTransactions',
        'referrer',
        'reminderDays',
        'requirePwdChange',
        'resaleNumber',
        'salesTeamList',
        'salutation',
        'sendEmail',
        'shipComplete',
        'stage',
        'startDate',
        'subscriptionsList',
        'symbolPlacement',
        'syncPartnerTeams',
        'taxExempt',
        'taxRegistrationList',
        'taxable',
        'thirdPartyAcct',
        'thirdPartyCountry',
        'thirdPartyZipcode',
        'title',
        'unbilledOrders',
        'url',
        'vatRegNumber',
        'visits',
        'webLead',
        'nullFieldList',
    ]

    RECORD_REF_FIELDS = [
        'accessRole',
        'assignedWebSite',
        'buyingReason',
        'buyingTimeFrame',
        'campaignCategory',
        'category',
        'customForm',
        'defaultTaxReg',
        'drAccount',
        'entityStatus',
        'fxAccount',
        'image',
        'leadSource',
        'openingBalanceAccount',
        'parent',
        'partner',
        'prefCCProcessor',
        'priceLevel',
        'receivablesAccount',
        'salesGroup',
        'salesReadiness',
        'salesRep',
        'shippingItem',
        'sourceWebSite',
        'taxItem',
        'terms',
        'territory',
    ]

    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='Customer')

    def post(self, data) -> OrderedDict:
        assert data['externalId'], 'missing external id'
        customer = self.ns_client.Customer(externalId=data['externalId'])

        customer['currency'] = self.ns_client.RecordRef(**(data['currency']))

        customer['subsidiary'] = self.ns_client.RecordRef(**(data['subsidiary']))

        customer['representingSubsidiary'] = self.ns_client.RecordRef(**(data['representingSubsidiary']))

        customer['monthlyClosing'] = self.ns_client.RecordRef(**(data['monthlyClosing']))

        self.build_simple_fields(self.SIMPLE_FIELDS, data, customer)

        self.build_record_ref_fields(self.RECORD_REF_FIELDS, data, customer)

        logger.debug('able to create customer = %s', customer)
        res = self.ns_client.upsert(customer)
        return self._serialize(res)
