from .base import ApiBase
from netsuitesdk.internal.utils import PaginatedSearch
import logging

logger = logging.getLogger(__name__)

class Items(ApiBase):

    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='Item')

    def get_all_generator(self, is_inactive=False):
        # Get Only Active Items using SearchBooleanField
        record_type_search_field = self.ns_client.SearchBooleanField(searchValue=is_inactive)
        basic_search = self.ns_client.basic_search_factory('Item', isInactive=record_type_search_field)

        paginated_search = PaginatedSearch(
            client=self.ns_client,
            type_name='Item',
            basic_search=basic_search,
            pageSize=20
        )

        return self._paginated_search_generator(paginated_search=paginated_search)

    def get_records_generator(self, last_modified_date=None, active=None):
        """
        Get items based on lastModifiedDate and active status
        :param last_modified_date: The date after which to search for items (YYYY-MM-DDT%HH:MM:SS)
        :param active: Boolean to filter by active status. None means no filter on active status
        :return: Generator of items matching the criteria
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
