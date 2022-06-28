import logging
import pytest
import json
import os

logger = logging.getLogger(__name__)

def load_je():
    filename = os.getenv('NS_ACCOUNT').lower() + '.json'
    with open('./test/integration/data/journal_entries/' + filename) as oj:
        s = oj.read()
        return json.loads(s)

def validate_je(expected, result):
    logger.debug('result = %s', result)
    assert result, f'No object with externalId'
    assert result['externalId'] == expected['externalId'], f'No object with externalId'
    assert result['currency']['name'] == expected['currency']['name'], f'Currency does not match'
    assert result['subsidiary']['internalId'] == expected['subsidiary']['internalId'], f'Subsidiary does not match'

def test_post(nc):
    je1 = load_je()
    logger.debug('rvb1 = %s', je1)
    res = nc.journal_entries.post(je1)
    logger.debug('res = %s', res)
    assert res['externalId'] == je1['externalId'], 'External ID does not match'
    assert res['type'] == 'journalEntry', 'Type does not match'

def test_get(nc):
    je1 = load_je()
    data = nc.journal_entries.get(externalId=je1['externalId'])
    validate_je(je1, data)

def test_get_all(nc):
    je1 = load_je()
    data = nc.journal_entries.get_all_generator()
    logger.debug('data = %s', data)
    assert data, 'get all generator didnt work'
    assert len(data) > 0, f'No data found'

    je = next(je for je in data if je['externalId'] == je1['externalId'])
    logger.debug('je = %s', je)
    validate_je(je1, je)
