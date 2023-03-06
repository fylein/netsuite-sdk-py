import os
import json
import logging

logger = logging.getLogger(__name__)

def test_post(nc):
    filename = os.getenv('NS_ACCOUNT').lower() + '.json'
    with open('./test/integration/data/credit_memo/' + filename) as oj:
        s = oj.read()
        credit_memo = json.loads(s)
    logger.debug('credit_memo = %s', credit_memo)
    res = nc.credit_memos.post(credit_memo)
    logger.debug('res = %s', res)
    assert res['externalId'] == credit_memo['externalId'], 'ID Number does not match'
    assert res['type'] == 'creditMemo', 'Type does not match'