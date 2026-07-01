from collections import OrderedDict

from netsuitesdk.internal.utils import PaginatedSearch

from .base import ApiBase
import logging

logger = logging.getLogger(__name__)


class Employees(ApiBase):
    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='Employee')

    def get_all_generator(self, is_inactive=False, page_size=50, last_modified_date_query={}):
        # Get Only Employee Items using SearchBooleanField
        record_type_search_field = self.ns_client.SearchBooleanField(searchValue=is_inactive)

        date_search = None
        if 'search_value' in last_modified_date_query and 'operator' in last_modified_date_query:
            if last_modified_date_query['search_value'] and last_modified_date_query['operator']:
                date_search = self.ns_client.SearchDateField(
                    searchValue=last_modified_date_query['search_value'],
                    operator=last_modified_date_query['operator']
                )

        basic_search = self.ns_client.basic_search_factory(
            type_name='Employee',
            isInactive=record_type_search_field,
            lastModifiedDate=date_search
        )

        paginated_search = PaginatedSearch(
            client=self.ns_client,
            type_name='Employee',
            basic_search=basic_search,
            pageSize=page_size
        )

        return self._paginated_search_generator(paginated_search=paginated_search)

    def get_records_generator(self, last_modified_date=None, active=None):
        """
        Get employees based on lastModifiedDate and active status
        :param last_modified_date: The date after which to search for employees (YYYY-MM-DDT%HH:MM:SS)
        :param active: Boolean to filter by active status. None means no filter on active status
        :return: Generator of employees matching the criteria
        """
        search_fields = {}

        if active is not None:
            search_fields['isInactive'] = self.ns_client.SearchBooleanField(
                searchValue=not active
            )

        if last_modified_date:
            search_fields['lastModifiedDate'] = self.ns_client.SearchDateField(
                searchValue=last_modified_date,
                operator='after'
            )

        basic_search = self.ns_client.basic_search_factory(
            type_name=self.type_name,
            **search_fields
        )

        paginated_search = PaginatedSearch(
            client=self.ns_client,
            type_name=self.type_name,
            basic_search=basic_search,
            pageSize=20
        )

        return self._paginated_search_generator(paginated_search=paginated_search)

    def post(self, data) -> OrderedDict:
        assert data['externalId'], 'missing external id'
        employee = self.ns_client.Employee(externalId=data['externalId'])

        employee['defaultExpenseReportCurrency'] = self.ns_client.RecordRef(**(data['defaultExpenseReportCurrency']))

        employee['subsidiary'] = self.ns_client.RecordRef(**(data['subsidiary']))

        employee['workCalendar'] = self.ns_client.RecordRef(**(data['workCalendar']))

        if 'defaultAcctCorpCardExp' in data and data['defaultAcctCorpCardExp']:
            employee['defaultAcctCorpCardExp'] = self.ns_client.RecordRef(**(data['defaultAcctCorpCardExp']))

        if 'entityId' in data:
            employee['entityId'] = data['entityId']

        if 'firstName' in data:
            employee['firstName'] = data['firstName']

        if 'lastName' in data:
            employee['lastName'] = data['lastName']

        if 'email' in data:
            employee['email'] = data['email']

        if 'inheritIPRules' in data:
            employee['inheritIPRules'] = data['inheritIPRules']

        if 'payFrequency' in data:
            employee['payFrequency'] = data['payFrequency']

        if 'location' in data:
            employee['location'] = data['location']

        if 'department' in data:
            employee['department'] = data['department']

        logger.debug('able to create employee = %s', employee)
        res = self.ns_client.upsert(employee)
        return self._serialize(res)
