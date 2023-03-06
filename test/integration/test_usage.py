import os
import json
import logging

logger = logging.getLogger(__name__)

def test_post(nc):
    filename = os.getenv('NS_ACCOUNT').lower() + '.json'
    with open('./test/integration/data/usage/' + filename) as oj:
        s = oj.read()
        usage = json.loads(s)
    logger.debug('credit_memo = %s', usage)
    res = nc.usages.post(usage)
    logger.debug('res = %s', res)
    assert res['externalId'] == usage['externalId'], 'ID Number does not match'
    assert res['type'] == 'creditMemo', 'Type does not match'