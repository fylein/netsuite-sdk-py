import logging
import os

import pytest
from netsuitesdk.zeep.client import NetSuiteClient

logger = logging.getLogger(__name__)

@pytest.fixture(scope='module')
def ns():
    """
    """
    NS_EMAIL = os.getenv("NS_EMAIL")
    NS_PASSWORD = os.getenv("NS_PASSWORD")
    NS_ROLE = os.getenv("NS_ROLE")
    NS_ACCOUNT = os.getenv("NS_ACCOUNT")
    NS_APPID = os.getenv("NS_APPID")

    ns = NetSuiteClient(account=NS_ACCOUNT)
    ns.login(email=NS_EMAIL, password=NS_PASSWORD, role=NS_ROLE, application_id=NS_APPID)
    return ns
