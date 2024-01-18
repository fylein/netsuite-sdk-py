from collections import OrderedDict
from netsuitesdk.internal.utils import PaginatedSearch

from .base import ApiBase
import logging

logger = logging.getLogger(__name__)


class JournalEntries(ApiBase):
    SIMPLE_FIELDS = [
        'memo',
        'tranDate',
        'tranId'
    ]

    RECORD_REF_FIELDS = [
        'class',
        'currency',
        'department',
        'location',
        'subsidiary',
        'toSubsidiary'
    ]

    TYPE_NAME = 'journalEntry'

    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name=self.TYPE_NAME)
        # Uppercase the first letter of the type name to get the class name
        self.class_name = self.type_name[:1].upper() + self.type_name[1:]
        self.class_ = getattr(ns_client, self.class_name)
        self.line_class_ = getattr(ns_client, self.class_name + 'Line')
        self.line_list_class_ = getattr(ns_client, self.class_name + 'LineList')

    def get_all_generator(self):
        record_type_search_field = self.ns_client.SearchStringField(searchValue=self.class_name, operator='contains')
        basic_search = self.ns_client.basic_search_factory('Transaction', recordType=record_type_search_field)
        paginated_search = PaginatedSearch(client=self.ns_client,
                                           type_name='Transaction',
                                           basic_search=basic_search,
                                           pageSize=20)
        return self._paginated_search_to_generator(paginated_search=paginated_search)

    def post(self, data) -> OrderedDict:
        assert data['externalId'], 'missing external id'
        je = self.class_(externalId=data['externalId'])
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
            jee = self.line_class_(**eod)
            line_list.append(jee)

        je['lineList'] = self.line_list_class_(line=line_list)
        self.build_simple_fields(self.SIMPLE_FIELDS, data, je)
        self.build_record_ref_fields(self.RECORD_REF_FIELDS, data, je)

        logger.debug('able to create je = %s', je)
        res = self.ns_client.upsert(je, 'journal_entry')
        return self._serialize(res)
