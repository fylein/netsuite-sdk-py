from collections import OrderedDict

from .base import ApiBase
import logging

from netsuitesdk.internal.utils import PaginatedSearch

logger = logging.getLogger(__name__)


class ExpenseReports(ApiBase):
    """
    ExpenseReports are not directly searchable - only via as employees
    """

    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='ExpenseReport')

    def get_all_generator(self):
        record_type_search_field = self.ns_client.SearchStringField(searchValue='ExpenseReport', operator='contains')
        basic_search = self.ns_client.basic_search_factory('Employee', recordType=record_type_search_field)
        paginated_search = PaginatedSearch(client=self.ns_client,
                                           type_name='Employee',
                                           basic_search=basic_search,
                                           pageSize=20)
        return self._paginated_search_to_generator(paginated_search=paginated_search)

    def post(self, data) -> OrderedDict:
        assert data['externalId'], 'missing external id'
        er = self.ns_client.ExpenseReport()
        expense_list = []
        for eod in data['expenseList']:
            if 'customFieldList' in eod and eod['customFieldList']:
                custom_fields = []
                for field in eod['customFieldList']:
                    if field['type'] == 'String':
                        custom_fields.append(
                            self.ns_client.StringCustomFieldRef(
                                scriptId=field['scriptId'] if 'scriptId' in field else None,
                                internalId=field['internalId'] if 'internalId' in field else None,
                                value=field['value']
                            )
                        )
                    elif field['type'] == 'Select':
                        custom_fields.append(
                            self.ns_client.SelectCustomFieldRef(
                                scriptId=field['scriptId'] if 'scriptId' in field else None,
                                internalId=field['internalId'] if 'internalId' in field else None,
                                value=self.ns_client.ListOrRecordRef(
                                    internalId=field['value']
                                )
                            )
                        )
                eod['customFieldList'] = self.ns_client.CustomFieldList(custom_fields)
            ere = self.ns_client.ExpenseReportExpense(**eod)
            expense_list.append(ere)

        er['expenseList'] = self.ns_client.ExpenseReportExpenseList(expense=expense_list)
        er['expenseReportCurrency'] = self.ns_client.RecordRef(**(data['expenseReportCurrency']))

        if 'memo' in data:
            er['memo'] = data['memo']

        if 'tranDate' in data:
            er['tranDate'] = data['tranDate']

        if 'tranId' in data:
            er['tranId'] = data['tranId']

        if 'class' in data:
            er['class'] = data['class']

        if 'location' in data:
            er['location'] = data['location']

        if 'department' in data:
            er['department'] = data['department']

        if 'account' in data:
            er['account'] = self.ns_client.RecordRef(**(data['account']))

        if 'accountingApproval' in data:
            er['accountingApproval'] = data['accountingApproval']

        if 'supervisorApproval' in data:
            er['supervisorApproval'] = data['supervisorApproval']

        if 'externalId' in data:
            er['externalId'] = data['externalId']

        er['entity'] = self.ns_client.RecordRef(**(data['entity']))
        logger.debug('able to create er = %s', er)
        res = self.ns_client.upsert(er)
        return self._serialize(res)
