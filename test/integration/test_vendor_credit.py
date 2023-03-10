import json
import os
import logging
import pytest

logger = logging.getLogger(__name__)

@pytest.mark.skip(reason="Can't test this due to persmission issues")
def test_post(nc):
    with open('./test/integration/data/vendor_credit/data.json') as oj:
        s = oj.read()
        vendor_credit = json.loads(s)
    logger.debug('vendor_credit = %s', vendor_credit)
    res = nc.vendor_credits.post(vendor_credit)
    logger.debug('res = %s', res)
    assert res['externalId'] == vendor_credit['externalId'], 'Transaction Number does not match'
    assert res['type'] == 'vendorCredit', 'Type does not match'
