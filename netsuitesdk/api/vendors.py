from collections import OrderedDict

from .base import ApiBase
import logging
from netsuitesdk.internal.utils import PaginatedSearch

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

    def get_records_generator(self, last_modified_date=None, active=None):
        """
        Get vendors based on lastModifiedDate and active status
        :param last_modified_date: The date after which to search for vendors (YYYY-MM-DDT%HH:MM:SS)
        :param active: Boolean to filter by active status. None means no filter on active status
        :return: Generator of vendors matching the criteria
        """
        search_fields = {}

        # Add active status filter if specified
        if active is not None:
            search_fields['isInactive'] = self.ns_client.SearchBooleanField(
                searchValue=not active
            )

        # Add last modified date filter if specified
        if last_modified_date:
            search_fields['lastModifiedDate'] = self.ns_client.SearchDateField(
                searchValue=last_modified_date,
                operator='after'
            )

        # Create basic search with the specified conditions
        basic_search = self.ns_client.basic_search_factory(
            type_name=self.type_name,
            **search_fields
        )

        # Create paginated search
        paginated_search = PaginatedSearch(
            client=self.ns_client,
            type_name=self.type_name,
            basic_search=basic_search,
            pageSize=20
        )

        # Return generator of results
        return self._paginated_search_generator(paginated_search=paginated_search)

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
