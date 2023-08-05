# coding: utf-8

"""
    Veeroute.Clustering

    Veeroute Clustering API  # noqa: E501

    The version of the OpenAPI document: 3.15.183137
    Contact: support@veeroute.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import vrt_lss_clustering
from vrt_lss_clustering.models.plan_info import PlanInfo  # noqa: E501
from vrt_lss_clustering.rest import ApiException

class TestPlanInfo(unittest.TestCase):
    """PlanInfo unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test PlanInfo
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_lss_clustering.models.plan_info.PlanInfo()  # noqa: E501
        if include_optional :
            return PlanInfo(
                status = 'FINISHED_IN_TIME', 
                result_version = 13, 
                planning_time = 10, 
                waiting_time = 5
            )
        else :
            return PlanInfo(
                status = 'FINISHED_IN_TIME',
        )

    def testPlanInfo(self):
        """Test PlanInfo"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
