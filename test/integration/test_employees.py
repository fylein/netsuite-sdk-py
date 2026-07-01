import os
import json
import logging

logger = logging.getLogger(__name__)

def test_post(nc):
    with open('./test/integration/data/employee/data.json') as oj:
        s = oj.read()
        employee = json.loads(s)
    logger.debug('employee = %s', employee)
    res = nc.employees.post(employee)
    logger.debug('res = %s', res)
    assert res['externalId'] == employee['externalId'], 'ID Number does not match'
    assert res['type'] == 'employee', 'Type does not match'


def test_get_records_generator(nc):
    data = []
    for records in nc.employees.get_records_generator(active=True):
        data.extend(records)
    logger.debug('data = %s', data)
    assert data, 'get records generator with active filter didnt work'

    modified_data = []
    for records in nc.employees.get_records_generator(last_modified_date='2020-01-01T00:00:00'):
        modified_data.extend(records)
    assert modified_data, 'get records generator with last_modified_date didnt work'