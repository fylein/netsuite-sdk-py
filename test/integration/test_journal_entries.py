import logging
import pytest
import json
import os

logger = logging.getLogger(__name__)

def test_get(nc):
    data = next(nc.journal_entries.get_all_generator())
    logger.debug('data = %s', data)
    assert data, 'get all generator didnt work'

    internal_id = data['internalId']
    data = nc.journal_entries.get(internalId=internal_id)
    logger.debug('data = %s', data)
    assert data, f'No object with internalId {internal_id}'

def test_post(nc):
    filename = os.getenv('NS_ACCOUNT').lower() + '.json'
    with open('./test/integration/data/journal_entries/' + filename) as oj:
        s = oj.read()
        je1 = json.loads(s)
    logger.debug('rvb1 = %s', je1)
    res = nc.journal_entries.post(je1)
    logger.debug('res = %s', res)
    assert res['externalId'] == je1['externalId'], 'External ID does not match'

    je2 = nc.journal_entries.get(externalId=res['externalId'])
    logger.debug('je2 = %s', je2)
