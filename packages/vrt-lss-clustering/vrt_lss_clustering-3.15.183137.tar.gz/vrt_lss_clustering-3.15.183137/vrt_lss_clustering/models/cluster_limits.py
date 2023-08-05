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


class ClusterLimits(object):
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
        'min_points': 'int',
        'max_points': 'int'
    }

    attribute_map = {
        'min_points': 'min_points',
        'max_points': 'max_points'
    }

    def __init__(self, min_points=1, max_points=1, local_vars_configuration=None):  # noqa: E501
        """ClusterLimits - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._min_points = None
        self._max_points = None
        self.discriminator = None

        if min_points is not None:
            self.min_points = min_points
        if max_points is not None:
            self.max_points = max_points

    @property
    def min_points(self):
        """Gets the min_points of this ClusterLimits.  # noqa: E501

        Minimum number of points in the cluster.  # noqa: E501

        :return: The min_points of this ClusterLimits.  # noqa: E501
        :rtype: int
        """
        return self._min_points

    @min_points.setter
    def min_points(self, min_points):
        """Sets the min_points of this ClusterLimits.

        Minimum number of points in the cluster.  # noqa: E501

        :param min_points: The min_points of this ClusterLimits.  # noqa: E501
        :type min_points: int
        """
        if (self.local_vars_configuration.client_side_validation and
                min_points is not None and min_points > 7000):  # noqa: E501
            raise ValueError("Invalid value for `min_points`, must be a value less than or equal to `7000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                min_points is not None and min_points < 1):  # noqa: E501
            raise ValueError("Invalid value for `min_points`, must be a value greater than or equal to `1`")  # noqa: E501

        self._min_points = min_points

    @property
    def max_points(self):
        """Gets the max_points of this ClusterLimits.  # noqa: E501

        Maximum number of points in the cluster.  # noqa: E501

        :return: The max_points of this ClusterLimits.  # noqa: E501
        :rtype: int
        """
        return self._max_points

    @max_points.setter
    def max_points(self, max_points):
        """Sets the max_points of this ClusterLimits.

        Maximum number of points in the cluster.  # noqa: E501

        :param max_points: The max_points of this ClusterLimits.  # noqa: E501
        :type max_points: int
        """
        if (self.local_vars_configuration.client_side_validation and
                max_points is not None and max_points > 7000):  # noqa: E501
            raise ValueError("Invalid value for `max_points`, must be a value less than or equal to `7000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                max_points is not None and max_points < 1):  # noqa: E501
            raise ValueError("Invalid value for `max_points`, must be a value greater than or equal to `1`")  # noqa: E501

        self._max_points = max_points

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
        if not isinstance(other, ClusterLimits):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ClusterLimits):
            return True

        return self.to_dict() != other.to_dict()
