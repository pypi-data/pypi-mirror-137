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
from vrt_lss_lastmile.models.transport import Transport  # noqa: E501
from vrt_lss_lastmile.rest import ApiException

class TestTransport(unittest.TestCase):
    """Transport unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Transport
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_lss_lastmile.models.transport.Transport()  # noqa: E501
        if include_optional :
            return Transport(
                key = 'transport0001', 
                transport_type = 'CAR', 
                transport_features = ["20T"], 
                performer_restrictions = ["Special"], 
                boxes = [
                    vrt_lss_lastmile.models.box.Box(
                        key = 'box01', 
                        capacity = vrt_lss_lastmile.models.capacity.Capacity(
                            mass = 10, 
                            volume = 2, 
                            capacity_x = 1, 
                            capacity_y = 2, 
                            capacity_z = 3, ), 
                        max_size = vrt_lss_lastmile.models.capacity.Capacity(
                            mass = 10, 
                            volume = 2, 
                            capacity_x = 1, 
                            capacity_y = 2, 
                            capacity_z = 3, ), 
                        width = 1, 
                        height = 3.1, 
                        length = 2.1, 
                        features = ["Freezer"], )
                    ], 
                max_boxes = 2, 
                max_capacity = vrt_lss_lastmile.models.capacity.Capacity(
                    mass = 10, 
                    volume = 2, 
                    capacity_x = 1, 
                    capacity_y = 2, 
                    capacity_z = 3, ), 
                attributes = ["Name:X51"]
            )
        else :
            return Transport(
                key = 'transport0001',
        )

    def testTransport(self):
        """Test Transport"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
