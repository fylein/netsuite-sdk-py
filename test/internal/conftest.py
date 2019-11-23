import logging
import os

import pytest
from netsuitesdk.internal.client import NetSuiteClient

logger = logging.getLogger(__name__)

@pytest.fixture(scope='module')
def ns():
    """
    Returns: (ns, headers)
    """
    NS_ACCOUNT = os.getenv('NS_ACCOUNT')
    NS_CONSUMER_KEY = os.getenv('NS_CONSUMER_KEY')
    NS_CONSUMER_SECRET = os.getenv('NS_CONSUMER_SECRET')
    NS_TOKEN_KEY = os.getenv('NS_TOKEN_KEY')
    NS_TOKEN_SECRET = os.getenv('NS_TOKEN_SECRET')
    ns = NetSuiteClient(account=NS_ACCOUNT)
    ns.connect_tba(consumer_key=NS_CONSUMER_KEY, consumer_secret=NS_CONSUMER_SECRET,
                                        token_key=NS_TOKEN_KEY, token_secret=NS_TOKEN_SECRET, signature_algorithm='HMAC-SHA1')
    return ns
