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
