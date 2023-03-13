import logging
import pytest
import zeep

logger = logging.getLogger(__name__)

@pytest.mark.parametrize('type_name', ['RecordList'])
def test_get_complex_type_element(ns, type_name):
    type_element = ns.get_complex_type_elements(complex_type = type_name)
    assert type_element == [('record', 'Record')]

@pytest.mark.parametrize('type_name', ['RecordList'])
def test_get_complex_type_info(ns, type_name):
    type_info = ns.get_complex_type_info(complex_type = type_name)
    assert type_info 

@pytest.mark.parametrize('type_name', ['RecordList'])
def test_get_complex_type_attributes(ns, type_name):
    type_attributes = ns.get_complex_type_attributes(complex_type = type_name)
    assert type_attributes == []