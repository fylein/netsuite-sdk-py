import logging
import pytest

logger = logging.getLogger(__name__)

def test_get(nc):
    data = nc.accounts.get_all()
    logger.debug('data = %s', data)
    assert data, 'get all didnt work'

    internal_id = data[0]['internalId']
    data = nc.accounts.get(internalId=internal_id)
    logger.debug('data = %s', data)
    assert data, f'No object with internalId {internal_id}'


def test_get_all_generator(nc):
    get_all_response = nc.accounts.get_all()
    get_all_generator_response = []
    for r in nc.accounts.get_all_generator(page_size=200):
        get_all_generator_response.append(r)
    len_get_all_genrator_respose = 0
    for i in get_all_generator_response:
        len_get_all_genrator_respose = len_get_all_genrator_respose + len(i)
    assert len(get_all_response) == len_get_all_genrator_respose, 'changing page size is returning different results'


def test_post(nc):
    data = {}
    with pytest.raises(NotImplementedError) as ex:
        nc.accounts.post(data)

