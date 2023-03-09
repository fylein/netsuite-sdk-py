import json
import os
import logging

logger = logging.getLogger(__name__)

def test_post(nc):
    filename = os.getenv('NS_ACCOUNT').lower() + '.json'
    with open('./test/integration/data/vendor_payment/' + filename) as oj:
        s = oj.read()
        vendor_payment = json.loads(s)
    logger.debug('vendor_payment = %s', vendor_payment)
    res = nc.vendor_payments.post(vendor_payment)
    logger.debug('res = %s', res)
    assert res['externalId'] == vendor_payment['externalId'], 'Transaction Number does not match'
    assert res['type'] == 'vendor_payment', 'Type does not match'
