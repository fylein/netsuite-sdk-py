

class User:

    def __init__(self, name, internalId, wsRole):
        """
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

    def __init__(self, client, type_name, basic_search=None, page_size=None, **kwargs):
        """
        :param NetSuiteClient client: the netsuite client proxy object
        :param str type_name: the type name to perform the search on
        :param int page_size: the number of records per result page
        """

        self._ns = client
        self._result = None
        self._type_name = type_name
        self._page_size = page_size or self.default_page_size
        self.basic_search = basic_search
        self.search(**kwargs)

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

    def search(self, **kwargs):
        """ Call the netsuite operation `search` """
        search_record = self._ns.search_factory(type_name=self._type_name)
        if self.basic_search is not None:
            search_record.basic = self.basic_search
        self._result = self._ns.search(searchRecord=search_record, pageSize=self._page_size, **kwargs)

    def goto_page(self, page_index):
        """ After search was performed, the netsuite operation `searchMoreWithId`
        can be used to retrieve more results """

        if self._result is None:
            return
        if page_index >= self.total_pages or page_index < 0:
            return
        self._result = self._ns.searchMoreWithId(
                                    searchId=self._result.searchId,
                                    pageIndex=page_index
        )
