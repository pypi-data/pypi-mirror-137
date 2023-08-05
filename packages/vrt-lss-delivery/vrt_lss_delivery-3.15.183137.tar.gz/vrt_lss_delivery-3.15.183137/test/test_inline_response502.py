# coding: utf-8

"""
    Veeroute.Delivery

    Veeroute Delivery API  # noqa: E501

    The version of the OpenAPI document: 3.15.183137
    Contact: support@veeroute.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import vrt_lss_delivery
from vrt_lss_delivery.models.inline_response502 import InlineResponse502  # noqa: E501
from vrt_lss_delivery.rest import ApiException

class TestInlineResponse502(unittest.TestCase):
    """InlineResponse502 unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test InlineResponse502
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_lss_delivery.models.inline_response502.InlineResponse502()  # noqa: E501
        if include_optional :
            return InlineResponse502(
                tracedata = vrt_lss_delivery.models.trace_data.TraceData(
                    code = 'client_server_service_time_uuid', 
                    client = 'client_name', 
                    server = 'server_name', 
                    service = 'LASTMILE', 
                    method = 'PLAN', 
                    time = '2021-02-21T09:30+03:00', ), 
                message = 'Bad Gateway', 
                code = 1502
            )
        else :
            return InlineResponse502(
                code = 1502,
        )

    def testInlineResponse502(self):
        """Test InlineResponse502"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
