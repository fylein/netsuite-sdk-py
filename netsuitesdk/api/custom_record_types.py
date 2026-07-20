from netsuitesdk.internal.utils import PaginatedSearch

from .base import ApiBase
import logging

logger = logging.getLogger(__name__)


class CustomRecordTypes(ApiBase):

    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='CustomRecordType')

    def _search_record(self, internalId):
        return self.ns_client.CustomRecordSearchBasic(
            recType=self.ns_client.CustomRecordType(
                internalId=internalId
            )
        )

    def count(self, internalId):
        cr_type = self._search_record(internalId)
        ps = PaginatedSearch(client=self.ns_client, type_name='CustomRecordType', search_record=cr_type, pageSize=1)
        return ps.total_records

    def get_all_by_id(self, internalId):
        cr_type = self._search_record(internalId)
        ps = PaginatedSearch(client=self.ns_client, type_name='CustomRecordType', search_record=cr_type, pageSize=20)
        return list(self._paginated_search_to_generator(paginated_search=ps))
