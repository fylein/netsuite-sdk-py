from .base import ApiBase


class VendorSubsidiaryRelationships(ApiBase):
    SIMPLE_FIELDS = [
    ]

    RECORD_REF_FIELDS = [
        'entity',
        'subsidiary',
    ]

    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='VendorSubsidiaryRelationship')
