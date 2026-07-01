import logging

logger = logging.getLogger(__name__)


def test_get_records_generator(nc):
    data = []
    for records in nc.projects.get_records_generator(active=True):
        data.extend(records)
    logger.debug('data = %s', data)
    assert data, 'get records generator with active filter didnt work'

    modified_data = []
    for records in nc.projects.get_records_generator(last_modified_date='2020-01-01T00:00:00'):
        modified_data.extend(records)
    assert modified_data, 'get records generator with last_modified_date didnt work'
