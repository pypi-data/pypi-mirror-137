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
from vrt_lss_delivery.models.facts import Facts  # noqa: E501
from vrt_lss_delivery.rest import ApiException

class TestFacts(unittest.TestCase):
    """Facts unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Facts
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_lss_delivery.models.facts.Facts()  # noqa: E501
        if include_optional :
            return Facts(
                order_facts = [
                    vrt_lss_delivery.models.order_fact.OrderFact(
                        type = 'DONE', 
                        time = '2021-05-21T09:30+03:00', 
                        order_key = 'order_01', 
                        job_facts = [
                            vrt_lss_delivery.models.job_fact.JobFact(
                                time = '2021-05-21T09:30+03:00', 
                                job_type = 'START_WORK', )
                            ], )
                    ], 
                performer_facts = [
                    vrt_lss_delivery.models.performer_fact.PerformerFact(
                        time = '2021-05-21T09:30+03:00', 
                        performer_key = 'performer_01', 
                        position = vrt_lss_delivery.models.track_point.TrackPoint(
                            latitude = 55.692789, 
                            longitude = 37.554554, 
                            time = '2021-05-21T19:45Z', ), )
                    ]
            )
        else :
            return Facts(
        )

    def testFacts(self):
        """Test Facts"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
