from collections import OrderedDict

from .base import ApiBase
import logging

logger = logging.getLogger(__name__)


class CustomRecords(ApiBase):
    SIMPLE_FIELDS = [
        'allowAttachments',
        'allowInlineEditing',
        'allowNumberingOverride',
        'allowQuickSearch',
        'altName',
        'autoName',
        'created',
        'customFieldList',
        'customRecordId',
        'description',
        'disclaimer',
        'enablEmailMerge',
        'enableNumbering',
        'includeName',
        'internalId',
        'isAvailableOffline',
        'isInactive',
        'isNumberingUpdateable',
        'isOrdered',
        'lastModified',
        'name',
        'numberingCurrentNumber',
        'numberingInit',
        'numberingMinDigits',
        'numberingPrefix',
        'numberingSuffix',
        'recordName',
        'scriptId',
        'showCreationDate',
        'showCreationDateOnList',
        'showId',
        'showLastModified',
        'showLastModifiedOnList',
        'showNotes',
        'showOwner',
        'showOwnerAllowChange',
        'showOwnerOnList',
        'translationsList',
        'usePermissions',
        'nullFieldList',
    ]

    RECORD_REF_FIELDS = [
        'customForm',
        'owner',
        'parent',
        'recType',
    ]

    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='CustomRecord')

    def post(self, data) -> OrderedDict:
        assert data['externalId'], 'missing external id'
        record = self.ns_client.CustomRecord(externalId=data['externalId'])

        self.build_simple_fields(self.SIMPLE_FIELDS, data, record)

        self.build_record_ref_fields(self.RECORD_REF_FIELDS, data, record)

        logger.debug('able to create custom record = %s', record)
        res = self.ns_client.upsert(record)
        return self._serialize(res)
