import logging
import os
import time

import pytest
from netsuitesdk.zeep.client import NetSuiteClient
from netsuitesdk.zeep.utils import PaginatedSearch

logger = logging.getLogger(__name__)

def test_login():
    """
    Test if login method is supported. We will not use this often.
    """
    NS_EMAIL = os.getenv("NS_EMAIL")
    NS_PASSWORD = os.getenv("NS_PASSWORD")
    NS_ROLE = os.getenv("NS_ROLE")
    NS_ACCOUNT = os.getenv("NS_ACCOUNT")
    NS_APPID = os.getenv("NS_APPID")
    ns = NetSuiteClient(account=NS_ACCOUNT)
    ns.login(email=NS_EMAIL, password=NS_PASSWORD, role=NS_ROLE, application_id=NS_APPID)
    type_name = 'Account'
    paginated_search = PaginatedSearch(client=ns, type_name=type_name, pageSize=20)
    assert len(paginated_search.records) > 0, f'There are no records of type {type_name}'
    logger.debug('record = %s', str(paginated_search.records[0]))
