import os
import json
import logging

logger = logging.getLogger(__name__)

def test_post(nc):
    with open('./test/integration/data/file/data.json') as oj:
        s = oj.read()
        file_data = json.loads(s)
    file_data['content'] = b"test_file"
    logger.debug('file_data = %s', file_data)
    res = nc.files.post(file_data)
    logger.debug('res = %s', res)
    assert res['externalId'] == file_data['externalId'], 'ID Number does not match'
    assert res['type'] == 'file', 'Type does not match'