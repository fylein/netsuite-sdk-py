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