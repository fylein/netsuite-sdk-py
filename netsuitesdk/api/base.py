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
        return list(self.get_all_generator())

    def get_all_generator(self, page_size=20):
        """
        Returns a generator which is more efficient memory-wise
        """
        return self._search_all_generator(page_size=page_size)

    def get(self, internalId=None, externalId=None) -> OrderedDict:
        return self._get(internalId=internalId, externalId=externalId)

    def get_ref(self, internalId=None, externalId=None) -> OrderedDict:
        return self._serialize(self.ns_client.RecordRef(type=self.type_name.lower(), internalId=internalId, externalId=externalId))

    def post(self, data) -> OrderedDict:
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

    def _paginated_search_to_generator(self, paginated_search):
        if paginated_search.num_records == 0:
            return

        num_pages = paginated_search.total_pages
        logger.debug('total pages = %d, records in page = %d', paginated_search.total_pages, paginated_search.num_records)
        logger.debug(f'current page index {paginated_search.page_index}')
        logger.debug('going to page %d', 0)

        num_records = paginated_search.num_records
        for r in range(0, num_records):
            record = paginated_search.records[r]
            yield self._serialize(record=record)

        for p in range(2, num_pages + 1):
            logger.debug('going to page %d', p)
            paginated_search.goto_page(p)
            logger.debug(f'current page index {paginated_search.page_index}')
            num_records = paginated_search.num_records
            for r in range(0, num_records):
                record = paginated_search.records[r]
                yield self._serialize(record=record)

    def _search_all_generator(self, page_size):
        ps = PaginatedSearch(client=self.ns_client, type_name=self.type_name, pageSize=page_size)
        return self._paginated_search_to_generator(paginated_search=ps)

    def _get_all(self) -> List[OrderedDict]:
        records = self.ns_client.getAll(recordType=self.type_name)
        return self._serialize_array(records)
    
    def _get_all_generator(self):
        res = self._get_all()
        for r in res:
            yield r

    def _get(self, internalId=None, externalId=None) -> OrderedDict:
        record = self.ns_client.get(recordType=self.type_name, internalId=internalId, externalId=externalId)
        return self._serialize(record=record)
