import logging
import pytest

logger = logging.getLogger(__name__)

def test_get(nc):
    data = nc.items.get_all_generator()
    logger.debug('data = %s', data)
    assert data, 'get all didnt work'

    internal_id = data[0]['internalId']
    data = nc.items.get(internalId=internal_id)
    logger.debug('data = %s', data)
    assert data, f'No object with internalId {internal_id}'
