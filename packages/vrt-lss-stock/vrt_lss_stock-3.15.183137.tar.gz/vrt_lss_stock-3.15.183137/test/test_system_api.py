# coding: utf-8

"""
    Veeroute.Stock

    Veeroute Stock API  # noqa: E501

    The version of the OpenAPI document: 3.15.183137
    Contact: support@veeroute.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import vrt_lss_stock
from vrt_lss_stock.api.system_api import SystemApi  # noqa: E501
from vrt_lss_stock.rest import ApiException


class TestSystemApi(unittest.TestCase):
    """SystemApi unit test stubs"""

    def setUp(self):
        self.api = vrt_lss_stock.api.system_api.SystemApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_check(self):
        """Test case for check

        Checking the service availability.  # noqa: E501
        """
        pass

    def test_version(self):
        """Test case for version

        Getting the service version.  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
