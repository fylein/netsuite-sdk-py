"""
Python Netsuite SDK using the SOAP client library
zeep(https://python-zeep.readthedocs.io/en/master/) to
connect to the NetSuite SOAP web service TalkSuite(http://www.netsuite.com/portal/platform/developer/suitetalk.shtml)
"""

import base64
import hashlib
import hmac
import logging
import os.path
import random
import sys
import time

from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport
from zeep.exceptions import Fault
from zeep.exceptions import LookupError as ZeepLookupError

from .exceptions import *

logging.basicConfig(stream=sys.stdout)
log = logging.getLogger(__name__)


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


class NetSuiteClient:
    """The Netsuite client class providing access to the Netsuite
    SOAP/WSDL web service"""

    DEFAULT_WSDL_URL = 'https://webservices.netsuite.com/wsdl/v2017_2_0/netsuite.wsdl'

    _complex_type_definitions = {
        'BaseRef': 'ns0:BaseRef',
        'GetAllRecord': 'ns0:GetAllRecord',
        'GetAllResult': 'ns0:GetAllResult',
        'Passport': 'ns0:Passport',
        'RecordList': 'ns0:RecordList',
        'RecordRef': 'ns0:RecordRef',
        'Status': 'ns0:Status',
        'StatusDetail': 'ns0:StatusDetail',
        'TokenPassport': 'ns0:TokenPassport',
        'TokenPassportSignature': 'ns0:TokenPassportSignature',
        'WsRole': 'ns0:WsRole',
        'ApplicationInfo': 'ns4:ApplicationInfo',
        'GetAllRequest': 'ns4:GetAllRequest',
        'GetResponse': 'ns4:GetResponse',
        'GetAllResponse': 'ns4:GetAllResponse',
        'PartnerInfo': 'ns4:PartnerInfo',

        'Account': 'ns17:Account',
    }

    _simple_type_definitions = {
        'RecordType': 'ns1:RecordType',
        'GetAllRecordType': 'ns1:GetAllRecordType',
    }

    def __init__(self, wsdl_url=None, caching=None, caching_timeout=None, debug=False):
        """
        Initialize the Zeep SOAP client, parse the xsd specifications
        of Netsuite and store the complex types as attributes of this
        instance.

        :param str wsdl_url: WSDL url of the Netsuite SOAP service.
                            If None, defaults to DEFAULT_WSDL_URL
        :param str caching: If caching = 'sqlite', setup Sqlite caching
        :param int caching_timeout: Timeout in seconds for caching.
                            If None, defaults to 30 days
        """

        if debug:
            log.setLevel(level=logging.DEBUG)
        else:
            log.setLevel(level=logging.WARNING)

        self._wsdl_url = wsdl_url or self.DEFAULT_WSDL_URL
        if caching == 'sqlite':
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache.db')
            timeout = caching_timeout or 30*24*60*60
            cache = SqliteCache(path=path, timeout=timeout)
            transport = Transport(cache=cache)
        else:
            transport = None

        # Initialize the Zeep Client
        self._client = Client(self._wsdl_url, transport=transport)

        # Parse all complex types specified in _complex_type_definitions
        # and store them as attributes of this instance
        self._init_complex_types()

        self._app_info = None
        self._is_authenticated = False
        self._user = None

    def _init_complex_types(self):
        self._complex_types = {}
        for k, v in self._complex_type_definitions.items():
            try:
                complex_type = self._client.get_type(v)
            except ZeepLookupError:
                log.warning('LookupError: Did not find complex type {}'.format(v))
            else:
                setattr(self, k, complex_type)
                self._complex_types[k] = complex_type

    def get_complex_type(self, type_name):
        return self._complex_types[type_name]

    def get_complex_type_attributes(self, type_name):
        complex_type = self.get_complex_type(type_name)
        return [(attribute.name, attribute.type) for attribute in complex_type._attributes]

    def create_passport(self, email, password, role, account):
        """
        Create a Passport object holding authentication credentials which
        will be passed to NetSuiteClient.login

        :param str email: NetSuite user email
        :param str password: NetSuite user password
        :param int role: Integer identifying the user role
        :param str account: the NetSuite account ID
        :rtype: Passport
        """

        role = self.RecordRef(internalId=role)
        return self.Passport(email=email, password=password, role=role, account=account)

    def create_token_passport(self, account, consumer_key, consumer_secret,
                              token_key, token_secret, signature_algorithm):
        """
        Create a TokenPassport object holding credentials for Token based
        authentication which will be passed to NetSuiteClient.login

        :param str account: the NetSuite account ID
        :param str consumer_key: the consumer key for the integration record
        :param str consumer_secret: the consumer secret
        :param str token_key: a string identifier of a token representing a
                        unique combination of a user, a role and an integration record
        :param str token_secret: the token secret
        :param str signature_algorithm: algorithm to compute the signature value (a hashed value),
                        choices are 'HMAC-SHA256' or 'HMAC-SHA1'
        :rtype: TokenPassport
        """

        def compute_nonce(length=20):
            """pseudo-random generated numeric string"""
            return ''.join([str(random.randint(0, 9)) for i in range(length)])

        nonce = compute_nonce(length=20)
        timestamp = int(time.time())
        key = '{}&{}'.format(consumer_secret, token_secret)
        base_string = '&'.join([account, consumer_key, token_key, nonce, str(timestamp)])
        key_bytes = key.encode(encoding='ascii')
        message_bytes = base_string.encode(encoding='ascii')
        # compute the signature
        if signature_algorithm == 'HMAC-SHA256':
            # hash
            hashed_value = hmac.new(key_bytes, msg=message_bytes, digestmod=hashlib.sha256)
        elif signature_algorithm == 'HMAC-SHA1':
            hashed_value = hmac.new(key_bytes, msg=message_bytes, digestmod=hashlib.sha1)
        else:
            raise NetSuiteError("signature_algorithm needs to be one of 'HMAC-SHA256', 'HMAC-SHA1'")

        dig = hashed_value.digest()
        # convert dig (a byte sequence) to a base 64 string
        value = base64.b64encode(dig).decode()

        signature = self.TokenPassportSignature(value, algorithm=signature_algorithm)
        return self.TokenPassport(account=account, consumerKey=consumer_key, token=token_key,
                                  nonce=nonce, timestamp=timestamp, signature=signature)

    def login(self, app_id, passport, fail_silently=False):
        """
        Authenticate and login user for a Netsuite session. The passport argument is
        of type Passport(email, password, role and account) which holds the credentials
        and can be created with NetSuiteClient.create_password.

        :param int app_id: All requests done in this session will be identified
            with this application Id.
        :param Passport passport: holds the credentials to authenticate the user.
        :param fail_silently: If True, will not reraise exceptions

        :return: the login response which contains the response status and user roles
        :rtype: LoginResponse
        :raises NetSuiteLoginError(message, code): if login was not successful. Possible codes
            are: InsufficientPermissionFault, InvalidAccountFault, InvalidSessionFault,
            InvalidCredentialsFault and UnexpectedErrorFault
        """

        if self._is_authenticated:
            self.logout()
        try:
            self._app_info = self.ApplicationInfo(applicationId=app_id)
            response = self._client.service.login(
                                passport,
                                _soapheaders={'applicationInfo': self._app_info}
            )
            if response.status.isSuccess:
                self._is_authenticated = True
                logged_in_role = self._log_roles(response)
                self._user = User(name=response.userId['name'],
                                  internalId=response.userId['internalId'],
                                  wsRole=logged_in_role)
                log.info("User {} logged in successfully.".format(str(self._user)))
                return response
            else:
                statusDetail = response.status['statusDetail'][0]
                exc = NetSuiteLoginError(
                            """An error occured in {operation} request:
                               \tmessage: {msg}""".format(operation=operation, msg=statusDetail['message']),
                            code=statusDetail['code']
                )
                log.error(str(exc))
                if not fail_silently:
                    raise exc
        except Fault as fault:
            exc = NetSuiteLoginError(str(fault), code=fault.code)
            log.error(str(exc))
            if not fail_silently:
                raise exc

    def _log_roles(self, response):
        roles = response.wsRoleList['wsRole']
        self._roles = []
        logged_in_role = None
        for role in roles:
            record_ref = self.RecordRef(name=role['role'].name,
                                        internalId=role['role'].internalId)
            wsRole = self.WsRole(
                        role=record_ref,
                        isDefault=role['isDefault'],
                        isInactive=role['isInactive'],
                        isLoggedInRole=role['isLoggedInRole']
                    )
            self._roles.append(wsRole)
            if wsRole.isLoggedInRole:
                logged_in_role = wsRole
        log.info('There are {} user roles: {}'.format(len(self._roles),
            ', '.join(['{}({})'.format(role.role.name, role.role.internalId) for role in self._roles])))
        return logged_in_role

    @property
    def logged_in(self):
        return self._is_authenticated

    def logout(self):
        if not self._is_authenticated:
            return
        response = self._client.service.logout()
        self._is_authenticated = False
        log.info("User {user} was logged out.".format(user=str(self._user)))
        self._user = None
        return response.status

