from .base import ApiBase
import logging

from ..internal.utils import PaginatedSearch

logger = logging.getLogger(__name__)

class ExpenseReports(ApiBase):
    """
    ExpenseReports are not directly searchable - only via as employees
    """
    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='ExpenseReport')

    def get_all_generator(self):
        record_type_search_field = self.ns_client.SearchStringField(searchValue='ExpenseReport', operator='contains')
        basic_search = self.ns_client.basic_search_factory('Employee', recordType=record_type_search_field)
        paginated_search = PaginatedSearch(client=self.ns_client,
                                        type_name='Employee',
                                        basic_search=basic_search,
                                        pageSize=20)
        return self._paginated_search_to_generator(paginated_search=paginated_search)
