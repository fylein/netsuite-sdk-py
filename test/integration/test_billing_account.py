import os
import json
import logging
import pytest

logger = logging.getLogger(__name__)

@pytest.mark.skip(reason="Can't test this due to persmission issues")
def test_post(nc):
    with open('./test/integration/data/billing_account/data.json') as oj:
        s = oj.read()
        billing_account = json.loads(s)
    logger.debug('billing_account = %s', billing_account)
    res = nc.billing_accounts.post(billing_account)
    logger.debug('res = %s', res)
    assert res['externalId'] == billing_account['externalId'], 'ID Number does not match'
    assert res['type'] == 'billingAccount', 'Type does not match'
