from netsuitesdk import NetSuiteClient

import os
import logging
import pytest

logger = logging.getLogger(__name__)

@pytest.fixture(scope='module')
def ns():
    """
    Returns: (ns, headers)
    """
    ACCOUNT_ID = os.getenv('ACCOUNT_ID')
    CONSUMER_KEY = os.getenv('CONSUMER_KEY')
    CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
    TOKEN_KEY = os.getenv('TOKEN_KEY')
    TOKEN_SECRET = os.getenv('TOKEN_SECRET')
    APP_ID = os.getenv('APP_ID')
    ns = NetSuiteClient(account=ACCOUNT_ID)
    ns.connect_tba(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET,
                                        token_key=TOKEN_KEY, token_secret=TOKEN_SECRET, signature_algorithm='HMAC-SHA1')
    return ns
 
# TODO: allow passing scope='module'.. cannot do that because the SDK messes with the headers passed
# @pytest.fixture
# def headers(ns):
#     ACCOUNT_ID = os.getenv('ACCOUNT_ID')
#     CONSUMER_KEY = os.getenv('CONSUMER_KEY')
#     CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
#     TOKEN_KEY = os.getenv('TOKEN_KEY')
#     TOKEN_SECRET = os.getenv('TOKEN_SECRET')
#     APP_ID = os.getenv('APP_ID')

#     tokenPassport = ns.create_token_passport()

#     headers_dict = {
#         'tokenPassport': tokenPassport
#     }
#     return headers_dict
