class PaginatedSearch:

    default_page_size = 20

    def __init__(self, client, type_name, search_record=None, basic_search=None, pageSize=None, perform_search=True):
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
        self.search_record = search_record or self._ns.search_factory(type_name=self._type_name)
        self.basic_search = basic_search
        if self.basic_search is not None:
            self.search_record.basic = self.basic_search
        if perform_search:
            self.search()

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

    def search(self):
        """ Call the netsuite operation `search` """
        self._result = self._ns.search(searchRecord=self.search_record)

    def goto_page(self, page_index):
        """ After a search was performed, this method utilizes the NetSuite
        operation `searchMoreWithId` to retrieve more results """

        if self._result is None:
            return
        if page_index > self.total_pages or page_index < 1:
            return
        self._result = self._ns.searchMoreWithId(searchId=self._result.searchId,
                                                 pageIndex=page_index)