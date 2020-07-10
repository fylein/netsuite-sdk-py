import logging
import pytest
import json
import os

logger = logging.getLogger(__name__)

def test_get(nc):
    data = next(nc.journal_entries.get_all_generator())
    logger.debug('data = %s', data)
    assert data, 'get all generator didnt work'
    assert data['internalId'] == '16', f'No object found with internalId'

    data = nc.journal_entries.get(externalId='JE_04')
    logger.debug('data = %s', data)
    currency = data['currency']
    assert data, f'No object with externalId'
    assert data['internalId'] == '10512', f'No object with internalId'
    assert data['externalId'] == 'JE_04', f'No object with externalId'
    assert currency['name'] == 'USA', f'Currency does not match'

def test_post(nc):
    filename = os.getenv('NS_ACCOUNT').lower() + '.json'
    with open('./test/integration/data/journal_entries/' + filename) as oj:
        s = oj.read()
        je1 = json.loads(s)
    logger.debug('rvb1 = %s', je1)
    res = nc.journal_entries.post(je1)
    logger.debug('res = %s', res)
    assert res['externalId'] == je1['externalId'], 'External ID does not match'
    assert res['type'] == 'journalEntry', 'Type does not match'

    je2 = nc.journal_entries.get(externalId=res['externalId'])
    currency = je2['currency']
    assert je2['internalId'] == '10512', f'No object with internalId'
    assert je2['externalId'] == 'JE_04', f'No object with externalId'
    assert currency['name'] == 'USA', f'Currency does not match'

    logger.debug('je2 = %s', je2)
