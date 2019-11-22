import zeep


logger = logging.getLogger(__name__)
 
class ApiBase:
    def __init__(self, ns_client, type_name):
        self.ns_client = ns_client
        self.type_name = type_name

    def get_all(self):
        return self._get_all()

    def get(self, external_id=None, internal_id=None):
        return self._get(external_id=external_id, internal_id=internal_id)

    def post(self, data):
        raise NotImplementedError('post method not implemented')

    @classmethod
    def _serialize(record):
        """
        record: single record
        Returns a dict
        """
        return zeep.helpers.serialize_object(record)

    @classmethod
    def _serialize_array(records):
        """
        records: a list of records
        Returns an array of dicts
        """
        return zeep.helpers.serialize_object(records)

    def _search_all(self):
        paginated_search = PaginatedSearch(client=self.ns_client, type_name=self.type_name, pageSize=20)
        # TODO: go over all the pages
        return ApiBase._serialize_array(paginated_search.records)

    def _get_all(self):
        records = ns.getAll(recordType=self.type_name)
        return ApiBase._serialize_array(records)
    
    def _get(self, internal_id=None, external_id=None):
        return self.ns_client.get(recordType=self.type_name, internalId=internal_id, externalId=external_id)

