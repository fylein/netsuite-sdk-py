import logging

logger = logging.getLogger(__name__)

def test_get(nc):
    data = nc.terms.get_all()
    logger.debug('data = %s', data)
    assert data, 'get all didnt work'

    internal_id = data[0]['internalId']
    data = nc.terms.get(internalId=internal_id)
    logger.debug('data = %s', data)
    assert data, f'No object with internalId {internal_id}'

def test_post(nc):
    term = {
        'dateDriven': None,
        'dayDiscountExpires': None,
        'dayOfMonthNetDue': None,
        'daysUntilExpiry': None,
        'daysUntilNetDue': 10,
        'discountPercent': None,
        'discountPercentDateDriven': None,
        'dueNextMonthIfWithinDays': None,
        'externalId': "testTermsAPI",
        'installment': None,
        'internalId': None,
        'isInactive': None,
        'name': "Test Term",
        'percentagesList': None,
        'preferred': None,
        'recurrenceCount': None,
        'recurrenceFrequency': None,
        'repeatEvery': None,
        'splitEvenly': None,
    }

    res = nc.terms.post(term)
    logger.debug('res = %s', res)
    assert res['externalId'] == term['externalId'], 'External ID does not match'
    assert res['type'] == 'term', 'Type does not match'

    expr2 = nc.terms.get(externalId=res['externalId'])
    logger.debug('expr2 = %s', expr2)
    assert expr2['externalId'] == term['externalId'], 'External ID does not match'
    assert expr2['name'] == term['name'], 'name does not match'
