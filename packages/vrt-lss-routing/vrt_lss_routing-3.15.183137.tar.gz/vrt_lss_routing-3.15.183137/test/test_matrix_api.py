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

import vrt_lss_routing
from vrt_lss_routing.api.matrix_api import MatrixApi  # noqa: E501
from vrt_lss_routing.rest import ApiException


class TestMatrixApi(unittest.TestCase):
    """MatrixApi unit test stubs"""

    def setUp(self):
        self.api = vrt_lss_routing.api.matrix_api.MatrixApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_build_matrix(self):
        """Test case for build_matrix

        Creating a time-distance matrix.  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
