from netsuitesdk.api.base import ApiBase
import logging
import pytest
from unittest import mock

logger = logging.getLogger(__name__)


@pytest.fixture
def instance():
    ns_client = mock.Mock()
    return ApiBase(ns_client, "type")


def test_build_simple_fields(instance):
    source_data = {
        'field1': 'value1',
        'field2': 'value2',
    }
    target = {}
    instance.build_simple_fields(['field1', 'field2'], source_data, target)

    assert target['field1'] == source_data['field1']
    assert target['field2'] == source_data['field2']


def test_build_record_ref_fields(instance):
    source_data = {
        'field1': {"externalId": "value1"},
        'field2': {"externalId": "value2"},
    }
    target = {}
    instance.build_record_ref_fields(['field1', 'field2'], source_data, target)

    assert target['field1'] == mock.ANY
    assert target['field1'] == mock.ANY
