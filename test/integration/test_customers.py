import logging
import json

logger = logging.getLogger(__name__)

def test_get(nc):
    data = nc.customers.get_all()
    logger.debug('data = %s', data)
    assert data, 'get all didnt work'

    internal_id = data[0]['internalId']
    data = nc.customers.get(internalId=internal_id)
    logger.debug('data = %s', data)
    assert data, f'No object with internalId {internal_id}'

def test_post(nc):
    with open('./test/integration/data/customers/customer.json') as oj:
        s = oj.read()
        expr1 = json.loads(s)
    logger.debug('expr1 = %s', expr1)
    res = nc.customers.post(expr1)
    logger.debug('res = %s', res)
    assert res['externalId'] == expr1['externalId'], 'External ID does not match'
    assert res['type'] == 'customer', 'Type does not match'

    expr2 = nc.customers.get(externalId=res['externalId'])
    logger.debug('expr2 = %s', expr2)
    assert expr2['externalId'] == expr1['externalId'], 'External ID does not match'
    assert expr2['companyName'] == expr1['companyName'], 'companyName does not match'
