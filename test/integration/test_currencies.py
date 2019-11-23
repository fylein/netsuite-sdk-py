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

def test_get_all_generator(nc):
    res1 = nc.currencies.get_all()
    res2 = []
    for r in nc.currencies.get_all_generator():
        res2.append(r)
    assert len(res1) == len(res2), 'get all and generator are returning different'

def test_post(nc):
    data = {}
    with pytest.raises(NotImplementedError) as ex:
        nc.currencies.post(data)
