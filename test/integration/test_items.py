import logging
import pytest

logger = logging.getLogger(__name__)

def test_get(nc):
    data = nc.items.get_all()
    logger.debug('data = %s', data)
    assert data, 'get all didnt work'
