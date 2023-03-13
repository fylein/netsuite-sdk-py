import logging
import pytest
import json
import os

logger = logging.getLogger(__name__)

def test_get(nc):
    data = nc.vendors.get_all()
    logger.debug('data = %s', data)
    assert data, 'get all didnt work'

    internal_id = data[0]['internalId']
    data = nc.vendors.get(internalId=internal_id)
    logger.debug('data = %s', data)
    assert data, f'No object with internalId {internal_id}'

def test_post(nc):
    with open('./test/integration/data/vendor/data.json') as oj:
        s = oj.read()
        vendor = json.loads(s)
    logger.debug('vendor = %s', vendor)
    res = nc.vendors.post(vendor)
    logger.debug('res = %s', res)
    assert res['externalId'] == vendor['externalId'], 'Transaction Number does not match'
    assert res['type'] == 'vendor', 'Type does not match'
