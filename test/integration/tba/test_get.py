from netsuitesdk import PaginatedSearch
import logging
import pytest
import zeep

logger = logging.getLogger(__name__)

def test_get_currency(ns):
    record = ns.get(recordType='currency', internalId='1')
    assert record, 'No currency record for internalId 1'
