import logging
import pytest

logger = logging.getLogger(__name__)

def test_get(nc):
    data = nc.currencies.get(internal_id='1')
    logger.info('data = %s', data)
    assert data, 'No currency with internal_id 1'
