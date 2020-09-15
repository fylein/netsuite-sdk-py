from collections import OrderedDict

from .base import ApiBase
import logging

logger = logging.getLogger(__name__)


class Files(ApiBase):
    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='File')

    def post(self, data) -> OrderedDict:
        assert data['externalId'], 'missing external id'
        file = self.ns_client.File()

        if 'name' in data:
            file['name'] = data['name']

        if 'folder' in data:
            file['folder'] = self.ns_client.RecordRef(**(data['folder']))

        if 'externalId' in data:
            file['externalId'] = data['externalId']

        if 'content' in data:
            file['content'] = data['content']

        if 'mediaType' in data:
            file['mediaType'] = data['mediaType']

        logger.debug('able to create file = %s', file)
        res = self.ns_client.upsert(file)
        return self._serialize(res)
