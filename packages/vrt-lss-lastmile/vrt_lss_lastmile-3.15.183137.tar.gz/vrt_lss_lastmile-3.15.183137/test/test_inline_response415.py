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
from vrt_lss_lastmile.models.inline_response415 import InlineResponse415  # noqa: E501
from vrt_lss_lastmile.rest import ApiException

class TestInlineResponse415(unittest.TestCase):
    """InlineResponse415 unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test InlineResponse415
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_lss_lastmile.models.inline_response415.InlineResponse415()  # noqa: E501
        if include_optional :
            return InlineResponse415(
                tracedata = vrt_lss_lastmile.models.trace_data.TraceData(
                    code = 'client_server_service_time_uuid', 
                    client = 'client_name', 
                    server = 'server_name', 
                    service = 'LASTMILE', 
                    method = 'PLAN', 
                    time = '2021-02-21T09:30+03:00', ), 
                message = 'Unsupported Media Type', 
                code = 1415
            )
        else :
            return InlineResponse415(
                code = 1415,
        )

    def testInlineResponse415(self):
        """Test InlineResponse415"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
