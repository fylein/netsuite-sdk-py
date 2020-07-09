import logging
import pytest
import json
import os

logger = logging.getLogger(__name__)

def test_get(nc):
    data = next(nc.expense_reports.get_all_generator())
    logger.debug('data = %s', data)
    assert data, 'get all generator didnt work'

    data = nc.expense_reports.get(externalId='EXPR_1')
    logger.debug('data = %s', data)
    assert data, f'No object with externalId'

def test_post(nc):
    filename = os.getenv('NS_ACCOUNT').lower() + '.json'
    with open('./test/integration/data/expense_reports/' + filename) as oj:
        s = oj.read()
        expr1 = json.loads(s)
    logger.debug('expr1 = %s', expr1)
    res = nc.expense_reports.post(expr1)
    logger.debug('res = %s', res)
    assert res['externalId'] == expr1['externalId'], 'External ID does not match'

    expr2 = nc.expense_reports.get(externalId=res['externalId'])
    logger.debug('expr2 = %s', expr2)
