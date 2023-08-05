# coding: utf-8

"""
    Veeroute.Routing

    Veeroute Routing API  # noqa: E501

    The version of the OpenAPI document: 3.15.183137
    Contact: support@veeroute.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import vrt_lss_routing
from vrt_lss_routing.models.version_result import VersionResult  # noqa: E501
from vrt_lss_routing.rest import ApiException

class TestVersionResult(unittest.TestCase):
    """VersionResult unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test VersionResult
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_lss_routing.models.version_result.VersionResult()  # noqa: E501
        if include_optional :
            return VersionResult(
                major = 2, 
                minor = 8, 
                build = 155426
            )
        else :
            return VersionResult(
                major = 2,
                minor = 8,
                build = 155426,
        )

    def testVersionResult(self):
        """Test VersionResult"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
