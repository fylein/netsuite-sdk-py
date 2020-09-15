from collections import OrderedDict

from .base import ApiBase
import logging

logger = logging.getLogger(__name__)


class Folders(ApiBase):
    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='Folder')

    def post(self, data) -> OrderedDict:
        assert data['externalId'], 'missing external id'
        folder = self.ns_client.Folder()

        if 'name' in data:
            folder['name'] = data['name']

        if 'externalId' in data:
            folder['externalId'] = data['externalId']

        logger.debug('able to create folder = %s', folder)
        res = self.ns_client.upsert(folder)
        return self._serialize(res)
