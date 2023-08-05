# coding: utf-8

"""
    Veeroute.Lastmile

    Veeroute Lastmile API  # noqa: E501

    The version of the OpenAPI document: 3.15.183137
    Contact: support@veeroute.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import vrt_lss_lastmile
from vrt_lss_lastmile.models.objects_metrics import ObjectsMetrics  # noqa: E501
from vrt_lss_lastmile.rest import ApiException

class TestObjectsMetrics(unittest.TestCase):
    """ObjectsMetrics unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ObjectsMetrics
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_lss_lastmile.models.objects_metrics.ObjectsMetrics()  # noqa: E501
        if include_optional :
            return ObjectsMetrics(
                keys = ["obj1"], 
                count = 1700
            )
        else :
            return ObjectsMetrics(
        )

    def testObjectsMetrics(self):
        """Test ObjectsMetrics"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
