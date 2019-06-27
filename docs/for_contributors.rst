For Contributors
====================

Todo
-----

	- In :mod:`netsuitesdk.netsuite_types` add missing types. Actually, at the moment only a fraction of all NetSuite types are listed. Even better: add utility functions to lookup the namespace which contains a NetSuite type. Maybe overwrite `__getattribute__` of class :class:`~netsuitesdk.client.NetSuiteClient`

	- Test and document token based authentication (in principle already implemented with :func:`~netsuitesdk.client.NetSuiteClient.create_token_passport()` and by passing created passport as `tokenPassport` in headers of requests like get, etc.)

	- Test and document more advanced search functionality (like join searches, ..).

	- Add & test netsuite operations: add, update, delete

	- Refactor all request functions like get, search, upsert, .. in :mod:`netsuitesdk.client` using decorator `request_service` 