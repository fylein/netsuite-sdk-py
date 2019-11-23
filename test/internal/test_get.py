from netsuitesdk.internal.utils import PaginatedSearch
import logging
import pytest

logger = logging.getLogger(__name__)

def test_get_currency(ns):
    record = ns.get(recordType='currency', internalId='1')
    assert record, 'No currency record for internalId 1'

def test_get_vendor_bill(ns):
    record = ns.get(recordType='vendorBill', externalId='1234')
    assert record, 'No vendor bill found'

# def test_get_currency1(nc):
#     currency = nc.currency.get(internal_id='1')
#     logger.info('currency is %s', currency)