import logging
import pytest

logger = logging.getLogger(__name__)

def test_get(nc):
    data = nc.vendor_bills.get_all()
    logger.info('data = %s', data)
    assert data, 'get all didnt work'

    internal_id = data[0]['internalId']
    data = nc.vendor_bills.get(internalId=internal_id)
    logger.info('data = %s', data)
    assert data, f'No object with internalId {internal_id}'
