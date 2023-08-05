# coding: utf-8

"""
    Veeroute.Account

    Veeroute Account Panel  # noqa: E501

    The version of the OpenAPI document: 3.15.183137
    Contact: support@veeroute.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import vrt_lss_account
from vrt_lss_account.api.auth_api import AuthApi  # noqa: E501
from vrt_lss_account.rest import ApiException


class TestAuthApi(unittest.TestCase):
    """AuthApi unit test stubs"""

    def setUp(self):
        self.api = vrt_lss_account.api.auth_api.AuthApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_change_password(self):
        """Test case for change_password

        Change password.  # noqa: E501
        """
        pass

    def test_generate_token(self):
        """Test case for generate_token

        Obtaining a token.  # noqa: E501
        """
        pass

    def test_validate_token(self):
        """Test case for validate_token

        Validating a token.  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
