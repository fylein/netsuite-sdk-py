import logging
import pytest

logger = logging.getLogger(__name__)

def test_get_all_by_id(nc):
    custom_record_type_response = nc.custom_record_types.get_all_by_id(476)
    assert custom_record_type_response[0]["recType"]["internalId"] == "476", "InternalId does not match"
    