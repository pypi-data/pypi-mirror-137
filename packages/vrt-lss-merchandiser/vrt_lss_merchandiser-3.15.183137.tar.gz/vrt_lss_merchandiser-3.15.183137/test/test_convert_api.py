# coding: utf-8

"""
    Veeroute.Merchandiser

    Veeroute Merchandiser API  # noqa: E501

    The version of the OpenAPI document: 3.15.183137
    Contact: support@veeroute.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import vrt_lss_merchandiser
from vrt_lss_merchandiser.api.convert_api import ConvertApi  # noqa: E501
from vrt_lss_merchandiser.rest import ApiException


class TestConvertApi(unittest.TestCase):
    """ConvertApi unit test stubs"""

    def setUp(self):
        self.api = vrt_lss_merchandiser.api.convert_api.ConvertApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_convert_to_json(self):
        """Test case for convert_to_json

        Conversion of planning task and result.  # noqa: E501
        """
        pass

    def test_convert_to_xlsx(self):
        """Test case for convert_to_xlsx

        Conversion of planning task and result.  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
