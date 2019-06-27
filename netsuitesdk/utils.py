"""
    :class:`User`: Represents a NetSuite user who is logged in
        via the NetSuiteClient class.

    :class:`PaginatedSearch`: utility class that can be used to perform a search.
"""

class User:

    def __init__(self, name, internalId, wsRole):
        """
        The User class represents a NetSuite user who is logged in
        via the NetSuiteClient class.

        :param str name: the user name
        :param int internalId: the id of the user
        :param WsRole wsRole: has attributes `role`(containing name
                and internalId of the role), `isDefault`, `isInactive` and `isLoggedInRole`
        """

        self.name = name
        self.internalId = internalId
        self.wsRole = wsRole

    def __str__(self):
        if self.wsRole is None:
            return self.name
        return '{}({})'.format(self.name, self.wsRole.role.name)


class PaginatedSearch:

    default_page_size = 20

    def __init__(self, client, type_name, search_record=None, basic_search=None, pageSize=None, perform_search=True, headers=None, **kwargs):
        """
        PaginatedSearch is a utility class that can be used to perform
        a search.

        :param NetSuiteClient client: the NetSuite client proxy object
        :param str type_name: the type name to perform the search on
        :param <record>Search search_record: object containing the search filters
        :param <record>SearchBasic basic_search: object containing basic search filters
        :param int pageSize: the number of records per result page
        :param bool perform_search: if True, will perform a first search after initializing basic data
        """

        self._ns = client
        self._result = None
        self._type_name = type_name
        kwargs['pageSize'] = pageSize or self.default_page_size
        self.search_record = search_record or self._ns.search_factory(type_name=self._type_name)
        self.basic_search = basic_search
        if self.basic_search is not None:
            self.search_record.basic = self.basic_search
        self._headers = headers
        if perform_search:
            self.search(headers=self._headers, **kwargs)

    @property
    def total_records(self):
        return self._result.totalRecords

    @property
    def page_size(self):
        return self._result.pageSize

    @property
    def total_pages(self):
        return self._result.totalPages

    @property
    def page_index(self):
        return self._result.pageIndex

    @property
    def records(self):
        return self._result.records

    @property
    def num_records(self):
        if self.records:
            return len(self.records)
        return 0

    def search(self, headers=None, **kwargs):
        """ Call the netsuite operation `search` """

        headers = headers or self._headers
        self._result = self._ns.search(searchRecord=self.search_record,
                                       headers=headers,
                                       **kwargs)

    def goto_page(self, page_index, headers=None, **kwargs):
        """ After a search was performed, this method utilizes the NetSuite
        operation `searchMoreWithId` to retrieve more results """

        if self._result is None:
            return
        if page_index > self.total_pages or page_index < 1:
            return
        headers = headers or self._headers
        self._result = self._ns.searchMoreWithId(searchId=self._result.searchId,
                                                 pageIndex=page_index,
                                                 headers=headers,
                                                 **kwargs)