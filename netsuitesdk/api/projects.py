from .base import ApiBase
import logging
from netsuitesdk.internal.utils import PaginatedSearch

logger = logging.getLogger(__name__)


class Projects(ApiBase):
    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='Job')

    def get_records_generator(self, last_modified_date=None, active=None):
        """
        Get projects based on lastModifiedDate and active status
        :param last_modified_date: The date after which to search for projects (YYYY-MM-DDT%HH:MM:SS)
        :param active: Boolean to filter by active status. None means no filter on active status
        :return: Generator of projects matching the criteria
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
