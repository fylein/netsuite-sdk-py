import logging
import os

import pytest
from netsuitesdk import NetSuiteConnection

logger = logging.getLogger(__name__)

@pytest.fixture(scope='module')
def nc():
    NS_ACCOUNT = os.getenv('NS_ACCOUNT')
    NS_CONSUMER_KEY = os.getenv('NS_CONSUMER_KEY')
    NS_CONSUMER_SECRET = os.getenv('NS_CONSUMER_SECRET')
    NS_TOKEN_KEY = os.getenv('NS_TOKEN_KEY')
    NS_TOKEN_SECRET = os.getenv('NS_TOKEN_SECRET')
    nc = NetSuiteConnection(account=NS_ACCOUNT, consumer_key=NS_CONSUMER_KEY, consumer_secret=NS_CONSUMER_SECRET, token_key=NS_TOKEN_KEY, token_secret=NS_TOKEN_SECRET)
    return nc
