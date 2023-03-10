import logging
import pytest
import json
import os

logger = logging.getLogger(__name__)

TYPE = 'journalEntry'
API = 'journal_entries'

class TestJournalEntries():

    @pytest.fixture(scope="class")
    def je(self):
        with open(f'./test/integration/data/{API}/data.json') as oj:
            s = oj.read()
            return json.loads(s)

    def get_api(self, nc):
        return getattr(nc, API)

    def validate_je(self, expected, result):
        logger.debug('result = %s', result)
        assert result, f'No object with externalId'
        assert result['internalId'] == expected['internalId'], f'Internal ID does not match'
        assert result['externalId'] == expected['externalId'], f'External ID does not match'
        assert result['currency']['name'] == expected['currency']['name'], f'Currency does not match'
        assert result['subsidiary']['internalId'] == expected['subsidiary']['internalId'], f'Subsidiary does not match'

    def validate_result(self, expected, result):
        logger.debug('result = %s', result)
        assert result['internalId'] == expected['internalId'], 'Internal ID does not match'
        assert result['externalId'] == expected['externalId'], 'External ID does not match'
        assert result['type'] == TYPE, 'Type does not match'

    def test_post(self, nc, je):
        api = self.get_api(nc)
        logger.debug('rvb1 = %s', je)

        # Test post of new journal entry
        res = api.post(je)
        je['internalId'] = res['internalId']
        self.validate_result(je, res)


    def test_get(self, nc, je):
        api = self.get_api(nc)
        data = api.get(externalId=je['externalId'])
        self.validate_je(je, data)

    def test_get_all(self, nc, je):
        api = self.get_api(nc)
        data = api.get_all_generator()
        logger.debug('data = %s', data)
        assert data, 'get all generator didnt work'
        assert len(data) > 0, f'No data found'

        je2 = next(je2 for je2 in data if je2['externalId'] == je['externalId'])
        self.validate_je(je, je2)

    def test_delete(self, nc, je):
        api = self.get_api(nc)
        res = api.delete(externalId=je['externalId'])
        self.validate_result(je, res)
