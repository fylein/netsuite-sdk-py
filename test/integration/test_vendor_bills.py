import logging
import pytest
import json
import os

logger = logging.getLogger(__name__)

def test_get(nc):
    data = next(nc.vendor_bills.get_all_generator())
    logger.debug('data = %s', data)
    assert data, 'get all generator didnt work'

    internal_id = data['internalId']
    data = nc.vendor_bills.get(internalId=internal_id)
    logger.debug('data = %s', data)
    assert data, f'No object with internalId {internal_id}'

def test_post(nc):
    filename = os.getenv('NS_ACCOUNT').lower() + '.json'
    vb1 = {}
    with open('./test/integration/data/vendor_bills/' + filename) as oj:
        s = oj.read()
        vb1 = json.loads(s)
    logger.debug('rvb1 = %s', vb1)
    res = nc.vendor_bills.post(vb1)
    logger.debug('res = %s', res)
    assert res['externalId'] == vb1['externalId'], 'External ID does not match'

    vb2 = nc.vendor_bills.get(externalId=res['externalId'])
    logger.debug('vb2 = %s', vb2)
    assert (29.99 < vb2['userTotal']) and (vb2['userTotal'] < 30.01), 'Bill total is not 30.0'

