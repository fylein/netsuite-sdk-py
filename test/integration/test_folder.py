import os
import json
import logging

logger = logging.getLogger(__name__)

def test_post(nc):
    filename = os.getenv('NS_ACCOUNT').lower() + '.json'
    with open('./test/integration/data/folder/' + filename) as oj:
        s = oj.read()
        folder_data = json.loads(s)
    logger.debug('file_data = %s', folder_data)
    res = nc.folders.post(folder_data)
    logger.debug('res = %s', res)
    assert res['externalId'] == folder_data['externalId'], 'ID Number does not match'
    assert res['type'] == 'folder', 'Type does not match'