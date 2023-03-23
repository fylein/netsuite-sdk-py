import logging
import pytest

logger = logging.getLogger(__name__)

@pytest.mark.skip(reason="customSegment is not a legal value for")
def test_get(nc):
    data = nc.custom_segments.get_all()
    logger.debug('data = %s', data)
    assert data, 'get all didnt work'

    internal_id = data[0]['internalId']
    data = nc.custom_segments.get(internalId=internal_id)
    logger.debug('data = %s', data)
    assert data, f'No object with internalId {internal_id}'

@pytest.mark.skip(reason="customSegment is not a legal value for")
def test_get_all_generator(nc):
    res1 = nc.custom_segments.get_all()
    res2 = []
    for r in nc.custom_segments.get_all_generator():
        res2.append(r)
    assert len(res1) == len(res2), 'get all and generator are returning different'