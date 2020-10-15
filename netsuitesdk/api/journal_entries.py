from collections import OrderedDict
from netsuitesdk.internal.utils import PaginatedSearch

from .base import ApiBase
import logging

logger = logging.getLogger(__name__)


class JournalEntries(ApiBase):
    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='journalEntry')

    def get_all_generator(self):
        record_type_search_field = self.ns_client.SearchStringField(searchValue='JournalEntry', operator='contains')
        basic_search = self.ns_client.basic_search_factory('Transaction', recordType=record_type_search_field)
        paginated_search = PaginatedSearch(client=self.ns_client,
                                           type_name='Transaction',
                                           basic_search=basic_search,
                                           pageSize=20)
        return self._paginated_search_to_generator(paginated_search=paginated_search)

    def post(self, data) -> OrderedDict:
        assert data['externalId'], 'missing external id'
        je = self.ns_client.JournalEntry(externalId=data['externalId'])
        line_list = []
        for eod in data['lineList']:
            if 'customFieldList' in eod and eod['customFieldList']:
                custom_fields = []
                for field in eod['customFieldList']:
                    if field['type'] == 'String':
                        custom_fields.append(
                            self.ns_client.StringCustomFieldRef(
                                scriptId=field['scriptId'] if 'scriptId' in field else None,
                                internalId=field['internalId'] if 'internalId' in field else None,
                                value=field['value']
                            )
                        )
                    elif field['type'] == 'Select':
                        custom_fields.append(
                            self.ns_client.SelectCustomFieldRef(
                                scriptId=field['scriptId'] if 'scriptId' in field else None,
                                internalId=field['internalId'] if 'internalId' in field else None,
                                value=self.ns_client.ListOrRecordRef(
                                    internalId=field['value']
                                )
                            )
                        )
                eod['customFieldList'] = self.ns_client.CustomFieldList(custom_fields)
            jee = self.ns_client.JournalEntryLine(**eod)
            line_list.append(jee)

        je['lineList'] = self.ns_client.JournalEntryLineList(line=line_list)
        je['currency'] = self.ns_client.RecordRef(**(data['currency']))

        if 'memo' in data:
            je['memo'] = data['memo']

        if 'tranDate' in data:
            je['tranDate'] = data['tranDate']

        if 'tranId' in data:
            je['tranId'] = data['tranId']

        if 'subsidiary' in data:
            je['subsidiary'] = data['subsidiary']

        if 'class' in data:
            je['class'] = data['class']

        if 'location' in data:
            je['location'] = data['location']

        if 'department' in data:
            je['department'] = data['department']

        logger.debug('able to create je = %s', je)
        res = self.ns_client.upsert(je)
        return self._serialize(res)
