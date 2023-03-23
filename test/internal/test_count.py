from netsuitesdk.internal.utils import PaginatedSearch
import logging
import pytest


@pytest.mark.parametrize('type_name', ['Account', 'Vendor', 'Department', 'Location', 'Classification', 'Subsidiary', 'Employee'])
def test_count(ns, type_name):
    ps = PaginatedSearch(client=ns, type_name=type_name, pageSize=10)
    assert ps.total_records > 0, 'Count cannot be 0'