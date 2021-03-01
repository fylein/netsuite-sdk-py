from collections import OrderedDict

from .base import ApiBase
import logging

logger = logging.getLogger(__name__)


class Employees(ApiBase):
    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='Employee')

    def post(self, data) -> OrderedDict:
        assert data['externalId'], 'missing external id'
        employee = self.ns_client.Employee(externalId=data['externalId'])

        employee['defaultExpenseReportCurrency'] = self.ns_client.RecordRef(**(data['defaultExpenseReportCurrency']))

        employee['subsidiary'] = self.ns_client.RecordRef(**(data['subsidiary']))

        employee['workCalendar'] = self.ns_client.RecordRef(**(data['workCalendar']))

        if 'entityId' in data:
            employee['entityId'] = data['entityId']

        if 'firstName' in data:
            employee['firstName'] = data['firstName']

        if 'lastName' in data:
            employee['lastName'] = data['lastName']

        if 'email' in data:
            employee['email'] = data['email']

        if 'inheritIPRules' in data:
            employee['inheritIPRules'] = data['inheritIPRules']

        if 'payFrequency' in data:
            employee['payFrequency'] = data['payFrequency']

        if 'location' in data:
            employee['location'] = data['location']

        if 'department' in data:
            employee['department'] = data['department']

        logger.debug('able to create employee = %s', employee)
        res = self.ns_client.upsert(employee)
        return self._serialize(res)
