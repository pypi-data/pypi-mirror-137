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
from vrt_lss_delivery.models.routing_matrix import RoutingMatrix  # noqa: E501
from vrt_lss_delivery.rest import ApiException

class TestRoutingMatrix(unittest.TestCase):
    """RoutingMatrix unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test RoutingMatrix
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_lss_delivery.models.routing_matrix.RoutingMatrix()  # noqa: E501
        if include_optional :
            return RoutingMatrix(
                waypoints = [
                    vrt_lss_delivery.models.waypoint.Waypoint(
                        name = 'central', 
                        latitude = 55.692789, 
                        longitude = 37.554554, 
                        duration = 15, )
                    ], 
                distances = [
                    [
                        1500
                        ]
                    ], 
                durations = [
                    [
                        1500
                        ]
                    ]
            )
        else :
            return RoutingMatrix(
                waypoints = [
                    vrt_lss_delivery.models.waypoint.Waypoint(
                        name = 'central', 
                        latitude = 55.692789, 
                        longitude = 37.554554, 
                        duration = 15, )
                    ],
                distances = [
                    [
                        1500
                        ]
                    ],
                durations = [
                    [
                        1500
                        ]
                    ],
        )

    def testRoutingMatrix(self):
        """Test RoutingMatrix"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
