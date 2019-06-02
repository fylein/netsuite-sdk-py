"""
For this example script, python-dotenv (pip install python-dotenv)
is used to load authentication parameters from a .env-file
as environment variables. The .env-file would look something like this:

NS_EMAIL = '*****@example.com'
NS_PASSWORD = '*******'
NS_ROLE = '1047'
NS_ACCOUNT = '*********'
NS_APPID = '********-****-****-****-************'

Alternatively, the variables can be set manually in the script.
"""

import os
from dotenv import load_dotenv

from netsuitesdk import NetSuiteClient


def test_login_with_credentials():
    load_dotenv()
    NS_EMAIL = os.getenv("NS_EMAIL")
    NS_PASSWORD = os.getenv("NS_PASSWORD")
    NS_ROLE = os.getenv("NS_ROLE")
    NS_ACCOUNT = os.getenv("NS_ACCOUNT")
    NS_APPID = os.getenv("NS_APPID")

    ns = NetSuiteClient(caching='sqlite', debug=True)

    # Login with user credentials (email, password, role and account)
    passport = ns.create_passport(email=NS_EMAIL,
                                  password=NS_PASSWORD,
                                  role=NS_ROLE,
                                  account=NS_ACCOUNT)
    ns.login(app_id=NS_APPID, passport=passport)

    # Test Get requests here. Not implemented yet.

    ns.logout()

def main():
    test_login_with_credentials()

if __name__ == '__main__':
    main()