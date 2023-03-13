import os
import json
import logging
import pytest

logger = logging.getLogger(__name__)

@pytest.mark.skip(reason="Can't test this due to persmission issues")
def test_post(nc):
    with open('./test/integration/data/invoices/data.json') as oj:
        s = oj.read()
        invoice = json.loads(s)
    logger.debug('invoice = %s', invoice)
    res = nc.invoices.post(invoice)
    logger.debug('res = %s', res)
    assert res['externalId'] == invoice['externalId'], 'ID Number does not match'
    assert res['type'] == 'invoice', 'Type does not match'