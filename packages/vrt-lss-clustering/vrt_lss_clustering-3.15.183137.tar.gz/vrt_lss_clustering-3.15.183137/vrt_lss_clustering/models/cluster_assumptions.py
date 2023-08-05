# coding: utf-8

"""
    Veeroute.Clustering

    Veeroute Clustering API  # noqa: E501

    The version of the OpenAPI document: 3.15.183137
    Contact: support@veeroute.com
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from vrt_lss_clustering.configuration import Configuration


class ClusterAssumptions(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'traffic_jams': 'bool',
        'flight_distance': 'bool'
    }

    attribute_map = {
        'traffic_jams': 'traffic_jams',
        'flight_distance': 'flight_distance'
    }

    def __init__(self, traffic_jams=True, flight_distance=False, local_vars_configuration=None):  # noqa: E501
        """ClusterAssumptions - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._traffic_jams = None
        self._flight_distance = None
        self.discriminator = None

        if traffic_jams is not None:
            self.traffic_jams = traffic_jams
        if flight_distance is not None:
            self.flight_distance = flight_distance

    @property
    def traffic_jams(self):
        """Gets the traffic_jams of this ClusterAssumptions.  # noqa: E501

        Accounting for traffic jams during clustering.  # noqa: E501

        :return: The traffic_jams of this ClusterAssumptions.  # noqa: E501
        :rtype: bool
        """
        return self._traffic_jams

    @traffic_jams.setter
    def traffic_jams(self, traffic_jams):
        """Sets the traffic_jams of this ClusterAssumptions.

        Accounting for traffic jams during clustering.  # noqa: E501

        :param traffic_jams: The traffic_jams of this ClusterAssumptions.  # noqa: E501
        :type traffic_jams: bool
        """

        self._traffic_jams = traffic_jams

    @property
    def flight_distance(self):
        """Gets the flight_distance of this ClusterAssumptions.  # noqa: E501

        Use it for calculating distances along a straight line. If `false` is specified, the distances are calculated by roads. When this parameter is enabled, traffic tracking (traffic_jams) is automatically disabled.   # noqa: E501

        :return: The flight_distance of this ClusterAssumptions.  # noqa: E501
        :rtype: bool
        """
        return self._flight_distance

    @flight_distance.setter
    def flight_distance(self, flight_distance):
        """Sets the flight_distance of this ClusterAssumptions.

        Use it for calculating distances along a straight line. If `false` is specified, the distances are calculated by roads. When this parameter is enabled, traffic tracking (traffic_jams) is automatically disabled.   # noqa: E501

        :param flight_distance: The flight_distance of this ClusterAssumptions.  # noqa: E501
        :type flight_distance: bool
        """

        self._flight_distance = flight_distance

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ClusterAssumptions):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ClusterAssumptions):
            return True

        return self.to_dict() != other.to_dict()
