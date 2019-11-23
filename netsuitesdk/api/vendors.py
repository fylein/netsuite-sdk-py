from .base import ApiBase
import logging

logger = logging.getLogger(__name__)

class Vendors(ApiBase):
    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='Vendor')
