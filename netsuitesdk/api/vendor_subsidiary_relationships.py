from collections import OrderedDict

from .base import ApiBase


class VendorSubsidiaryRelationships(ApiBase):
    RECORD_REF_FIELDS = [
        'entity',
        'subsidiary',
    ]

    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='VendorSubsidiaryRelationship')

    def _build_vendor_subsidiary_relationship(self, data) -> OrderedDict:
        assert data['externalId'], 'missing external id'
        vsr = self.ns_client.VendorSubsidiaryRelationship(externalId=data['externalId'])
        self.build_record_ref_fields(self.RECORD_REF_FIELDS, data, vsr)
        return vsr

    def post(self, data) -> OrderedDict:
        vsr = self._build_vendor_subsidiary_relationship(data)
        response = self.ns_client.upsert(vsr)
        return self._serialize(response)

    def post_batch(self, records) -> [OrderedDict]:
        vsrs = [self._build_vendor_subsidiary_relationship(record) for record in records]
        responses = self.ns_client.upsert_list(vsrs)
        return [self._serialize(response) for response in responses]
