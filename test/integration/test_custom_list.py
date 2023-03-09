import logging
import pytest

logger = logging.getLogger(__name__)

@pytest.mark.skip(reason="Can't test this due to persmission issues")
def test_get(nc):
    data = nc.custom_lists.get_all()
    logger.debug('data = %s', data)
    assert data, 'get all didnt work'

    internal_id = data[0]['internalId']
    data = nc.custom_lists.get(internalId=internal_id)
    logger.debug('data = %s', data)
    assert data, f'No object with internalId {internal_id}'

@pytest.mark.skip(reason="Can't test this due to persmission issues")
def test_get_all_generator(nc):
    res1 = nc.custom_lists.get_all()
    res2 = []
    for r in nc.custom_lists.get_all_generator():
        res2.append(r)
    assert len(res1) == len(res2), 'get all and generator are returning different'