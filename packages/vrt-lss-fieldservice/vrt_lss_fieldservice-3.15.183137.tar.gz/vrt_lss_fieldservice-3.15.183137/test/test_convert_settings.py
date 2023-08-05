# coding: utf-8

"""
    Veeroute.Fieldservice

    Veeroute Field Service Engineers API  # noqa: E501

    The version of the OpenAPI document: 3.15.183137
    Contact: support@veeroute.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import vrt_lss_fieldservice
from vrt_lss_fieldservice.models.convert_settings import ConvertSettings  # noqa: E501
from vrt_lss_fieldservice.rest import ApiException

class TestConvertSettings(unittest.TestCase):
    """ConvertSettings unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ConvertSettings
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_lss_fieldservice.models.convert_settings.ConvertSettings()  # noqa: E501
        if include_optional :
            return ConvertSettings(
                route_index_from = 15, 
                route_index_to = 150
            )
        else :
            return ConvertSettings(
        )

    def testConvertSettings(self):
        """Test ConvertSettings"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
