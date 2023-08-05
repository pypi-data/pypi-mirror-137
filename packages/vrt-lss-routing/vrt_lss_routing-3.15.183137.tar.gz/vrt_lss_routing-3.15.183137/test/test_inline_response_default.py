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
from vrt_lss_routing.models.inline_response_default import InlineResponseDefault  # noqa: E501
from vrt_lss_routing.rest import ApiException

class TestInlineResponseDefault(unittest.TestCase):
    """InlineResponseDefault unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test InlineResponseDefault
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_lss_routing.models.inline_response_default.InlineResponseDefault()  # noqa: E501
        if include_optional :
            return InlineResponseDefault(
                tracedata = vrt_lss_routing.models.trace_data.TraceData(
                    code = 'client_server_service_time_uuid', 
                    client = 'client_name', 
                    server = 'server_name', 
                    service = 'LASTMILE', 
                    method = 'PLAN', 
                    time = '2021-02-21T09:30+03:00', ), 
                message = 'Unexpected Server Error', 
                code = 1599
            )
        else :
            return InlineResponseDefault(
        )

    def testInlineResponseDefault(self):
        """Test InlineResponseDefault"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
