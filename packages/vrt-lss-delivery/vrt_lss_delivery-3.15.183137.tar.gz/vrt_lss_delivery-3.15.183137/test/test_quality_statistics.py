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
from vrt_lss_delivery.models.quality_statistics import QualityStatistics  # noqa: E501
from vrt_lss_delivery.rest import ApiException

class TestQualityStatistics(unittest.TestCase):
    """QualityStatistics unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test QualityStatistics
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_lss_delivery.models.quality_statistics.QualityStatistics()  # noqa: E501
        if include_optional :
            return QualityStatistics(
                soft_time_window_violations = vrt_lss_delivery.models.time_window_violation.TimeWindowViolation(
                    before = vrt_lss_delivery.models.objects_metrics.ObjectsMetrics(
                        keys = ["obj1"], 
                        count = 1700, ), 
                    after = vrt_lss_delivery.models.objects_metrics.ObjectsMetrics(
                        keys = ["obj1"], 
                        count = 1700, ), ), 
                hard_time_window_violations = vrt_lss_delivery.models.time_window_violation.TimeWindowViolation(
                    before = vrt_lss_delivery.models.objects_metrics.ObjectsMetrics(
                        keys = ["obj1"], 
                        count = 1700, ), 
                    after = vrt_lss_delivery.models.objects_metrics.ObjectsMetrics(
                        keys = ["obj1"], 
                        count = 1700, ), )
            )
        else :
            return QualityStatistics(
                soft_time_window_violations = vrt_lss_delivery.models.time_window_violation.TimeWindowViolation(
                    before = vrt_lss_delivery.models.objects_metrics.ObjectsMetrics(
                        keys = ["obj1"], 
                        count = 1700, ), 
                    after = vrt_lss_delivery.models.objects_metrics.ObjectsMetrics(
                        keys = ["obj1"], 
                        count = 1700, ), ),
                hard_time_window_violations = vrt_lss_delivery.models.time_window_violation.TimeWindowViolation(
                    before = vrt_lss_delivery.models.objects_metrics.ObjectsMetrics(
                        keys = ["obj1"], 
                        count = 1700, ), 
                    after = vrt_lss_delivery.models.objects_metrics.ObjectsMetrics(
                        keys = ["obj1"], 
                        count = 1700, ), ),
        )

    def testQualityStatistics(self):
        """Test QualityStatistics"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
