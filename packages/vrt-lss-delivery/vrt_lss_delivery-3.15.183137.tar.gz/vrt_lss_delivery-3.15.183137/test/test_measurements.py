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
from vrt_lss_delivery.models.measurements import Measurements  # noqa: E501
from vrt_lss_delivery.rest import ApiException

class TestMeasurements(unittest.TestCase):
    """Measurements unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Measurements
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_lss_delivery.models.measurements.Measurements()  # noqa: E501
        if include_optional :
            return Measurements(
                driving_time = 15, 
                waiting_time = 5, 
                working_time = 50, 
                arriving_time = 30, 
                departure_time = 20, 
                total_time = 120, 
                distance = 5200, 
                time_window = vrt_lss_delivery.models.time_window.TimeWindow(
                    from = '2021-02-21T09:30+03:00', 
                    to = '2021-02-21T19:45Z', )
            )
        else :
            return Measurements(
                driving_time = 15,
                waiting_time = 5,
                working_time = 50,
                arriving_time = 30,
                departure_time = 20,
                total_time = 120,
                distance = 5200,
        )

    def testMeasurements(self):
        """Test Measurements"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
