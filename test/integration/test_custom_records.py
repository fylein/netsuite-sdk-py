import os
import json
import logging

logger = logging.getLogger(__name__)

def test_post(nc):
    filename = os.getenv('NS_ACCOUNT').lower() + '.json'
    with open('./test/integration/data/custom_record/' + filename) as oj:
        s = oj.read()
        custom_record = json.loads(s)
    logger.debug('custom_record = %s', custom_record)
    res = nc.custom_records.post(custom_record)
    logger.debug('res = %s', res)
    assert res['externalId'] == custom_record['externalId'], 'ID Number does not match'