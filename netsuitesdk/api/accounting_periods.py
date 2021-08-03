from .base import ApiBase
import logging

logger = logging.getLogger(__name__)

class AccountingPeriod(ApiBase):

    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='AccountingPeriod')

    def search(self, attribute, value, operator):
        """
        Search Record
        :param attribute: name of the field, eg. entityId
        :param value: value of the field, eg. Amazon
        :param operator: search matching operator, eg., 'contains', 'is', 'anyOf'
        :return:
        """
        records = self.ns_client.basic_stringfield_search(
            type_name=self.type_name,
            attribute=attribute,
            value=value,
            operator=operator
        )

        return records