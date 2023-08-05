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
import datetime

import vrt_lss_account
from vrt_lss_account.models.service_quota import ServiceQuota  # noqa: E501
from vrt_lss_account.rest import ApiException

class TestServiceQuota(unittest.TestCase):
    """ServiceQuota unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ServiceQuota
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_lss_account.models.service_quota.ServiceQuota()  # noqa: E501
        if include_optional :
            return ServiceQuota(
                service = 'LASTMILE', 
                methods = [
                    vrt_lss_account.models.method_quota.MethodQuota(
                        method = 'PLAN', 
                        points_per_request = 15, 
                        points_per_day = 1500, 
                        points_per_date_window = 1500, 
                        max_concurrent_execution = 5, )
                    ]
            )
        else :
            return ServiceQuota(
                service = 'LASTMILE',
                methods = [
                    vrt_lss_account.models.method_quota.MethodQuota(
                        method = 'PLAN', 
                        points_per_request = 15, 
                        points_per_day = 1500, 
                        points_per_date_window = 1500, 
                        max_concurrent_execution = 5, )
                    ],
        )

    def testServiceQuota(self):
        """Test ServiceQuota"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
