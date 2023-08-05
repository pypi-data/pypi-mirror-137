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
import datetime

import vrt_lss_merchandiser
from vrt_lss_merchandiser.models.location import Location  # noqa: E501
from vrt_lss_merchandiser.rest import ApiException

class TestLocation(unittest.TestCase):
    """Location unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Location
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_lss_merchandiser.models.location.Location()  # noqa: E501
        if include_optional :
            return Location(
                latitude = 55.692789, 
                longitude = 37.554554, 
                arrival_duration = 15, 
                departure_duration = 5
            )
        else :
            return Location(
                latitude = 55.692789,
                longitude = 37.554554,
        )

    def testLocation(self):
        """Test Location"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
