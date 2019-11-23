import zeep
import logging
from collections import OrderedDict
from netsuitesdk.internal.utils import PaginatedSearch
from typing import List

logger = logging.getLogger(__name__)
 
 # TODO: introduce arg and return types
class ApiBase:
    def __init__(self, ns_client, type_name):
        self.ns_client = ns_client
        self.type_name = type_name

    def get_all(self):
        return self._search_all()

    def get(self, internalId=None, externalId=None) -> OrderedDict:
        return self._get(internalId=internalId, externalId=externalId)

    def post(self, data):
        raise NotImplementedError('post method not implemented')

    def _serialize(self, record) -> OrderedDict:
        """
        record: single record
        Returns a dict
        """
        return zeep.helpers.serialize_object(record)

    def _serialize_array(self, records) -> List[OrderedDict]:
        """
        records: a list of records
        Returns an array of dicts
        """
        return zeep.helpers.serialize_object(records)

    def _search_all(self) -> List[OrderedDict]:
        paginated_search = PaginatedSearch(client=self.ns_client, type_name=self.type_name, pageSize=20)
        # TODO: go over all the pages
        return self._serialize_array(paginated_search.records)

    def _get_all(self) -> List[OrderedDict]:
        records = self.ns_client.getAll(recordType=self.type_name)
        return self._serialize_array(records)
    
    def _get(self, internalId=None, externalId=None) -> OrderedDict:
        record = self.ns_client.get(recordType=self.type_name, internalId=internalId, externalId=externalId)
        return self._serialize(record=record)
