import logging
import os
import time

import pytest
from netsuitesdk.internal.client import NetSuiteClient
from netsuitesdk.internal.utils import PaginatedSearch

logger = logging.getLogger(__name__)

def test_logout():
    """
    Test if logout method is supported. We will not use this often.
    """
    NS_ACCOUNT = os.getenv("NS_ACCOUNT")    
    ns = NetSuiteClient(account=NS_ACCOUNT)
    ns.logout()
