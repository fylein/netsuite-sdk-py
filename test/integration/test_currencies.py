import logging
import pytest

logger = logging.getLogger(__name__)

def test_get(nc):
    data = nc.currencies.get_all()
    logger.debug('data = %s', data)
    assert data, 'get all didnt work'

    internal_id = data[0]['internalId']
    data = nc.currencies.get(internalId=internal_id)
    logger.debug('data = %s', data)
    assert data, f'No object with internalId {internal_id}'
