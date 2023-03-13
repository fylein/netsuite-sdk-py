import json
import os
import logging

logger = logging.getLogger(__name__)

def test_get(nc):
    get_all_respose = nc.vendor_payments.get_all()
    get_all_generator_response = []
    for r in nc.vendor_payments.get_all_generator():
        get_all_generator_response.append(r)
    len_get_all_generator_response = 0
    for i in get_all_generator_response:
        len_get_all_generator_response += len(i)
    assert len(get_all_respose) == len_get_all_generator_response, 'changing page size is returning different results'
    

def test_post(nc):
    with open('./test/integration/data/vendor_payment/data.json') as oj:
        s = oj.read()
        vendor_payment = json.loads(s)
    logger.debug('vendor_payment = %s', vendor_payment)
    res = nc.vendor_payments.post(vendor_payment)
    logger.debug('res = %s', res)
    assert res['externalId'] == vendor_payment['externalId'], 'Transaction Number does not match'
    assert res['type'] == 'vendorPayment', 'Type does not match'
