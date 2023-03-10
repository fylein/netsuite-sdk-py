import os
import json
import logging
import pytest

logger = logging.getLogger(__name__)


@pytest.mark.skip(reason="Can't test this due to persmission issues")
def test_post(nc):
    with open('./test/integration/data/usage/data.json') as oj:
        s = oj.read()
        usage = json.loads(s)
    logger.debug('credit_memo = %s', usage)
    res = nc.usages.post(usage)
    logger.debug('res = %s', res)
    assert res['externalId'] == usage['externalId'], 'ID Number does not match'
    assert res['type'] == 'creditMemo', 'Type does not match'