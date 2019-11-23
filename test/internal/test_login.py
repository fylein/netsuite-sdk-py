import logging
import os
import time

import pytest
from netsuitesdk.internal.client import NetSuiteClient
from netsuitesdk.internal.utils import PaginatedSearch
from netsuitesdk.internal.exceptions import NetSuiteLoginError

logger = logging.getLogger(__name__)

def test_login_disallowed():
    """
    Test if login method is supported. We will not use this often.
    """
    NS_EMAIL = os.getenv("NS_EMAIL")
    NS_PASSWORD = os.getenv("NS_PASSWORD")
    NS_ROLE = os.getenv("NS_ROLE")
    NS_ACCOUNT = os.getenv("NS_ACCOUNT")
    NS_APPID = os.getenv("NS_APPID")
    ns = NetSuiteClient(account=NS_ACCOUNT)
    with pytest.raises(NetSuiteLoginError) as ex:
        ns.login(email=NS_EMAIL, password=NS_PASSWORD, role=NS_ROLE, application_id=NS_APPID)
    assert 'Integration blocked' in str(ex.value), 'credentials are allowing login - this is not recommended'
