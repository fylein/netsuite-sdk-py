import logging
import pytest

logger = logging.getLogger(__name__)

def test_get(nc):
    data = nc.subsidiaries.get_all()
    logger.debug('data = %s', data)
    assert data, 'get all didnt work'

    internal_id = data[0]['internalId']
    data = nc.subsidiaries.get(internalId=internal_id)
    logger.debug('data = %s', data)
    assert data, f'No object with internalId {internal_id}'

def test_get_all_generator(nc):
    get_all_response = nc.subsidiaries.get_all()
    get_all_generator_response = []
    for r in nc.subsidiaries.get_all_generator(page_size=200):
        get_all_generator_response.append(r)
    len_get_all_generator_response = 0
    for i in get_all_generator_response:
        len_get_all_generator_response += len(i)
    assert len(get_all_response) == len_get_all_generator_response, 'changing page size is returning different results'

def test_post(nc):
    data = {}
    with pytest.raises(NotImplementedError) as ex:
        nc.subsidiaries.post(data)
