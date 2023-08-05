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


class Validation(object):
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
        'type': 'str',
        'entity_key': 'str',
        'entity_type': 'str',
        'info': 'str'
    }

    attribute_map = {
        'type': 'type',
        'entity_key': 'entity_key',
        'entity_type': 'entity_type',
        'info': 'info'
    }

    def __init__(self, type=None, entity_key=None, entity_type=None, info=None, local_vars_configuration=None):  # noqa: E501
        """Validation - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._type = None
        self._entity_key = None
        self._entity_type = None
        self._info = None
        self.discriminator = None

        self.type = type
        if entity_key is not None:
            self.entity_key = entity_key
        if entity_type is not None:
            self.entity_type = entity_type
        self.info = info

    @property
    def type(self):
        """Gets the type of this Validation.  # noqa: E501

        Validation type: * `info`  * `warning`  * `error`    # noqa: E501

        :return: The type of this Validation.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Validation.

        Validation type: * `info`  * `warning`  * `error`    # noqa: E501

        :param type: The type of this Validation.  # noqa: E501
        :type type: str
        """
        if self.local_vars_configuration.client_side_validation and type is None:  # noqa: E501
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        allowed_values = ["info", "warning", "error"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and type not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def entity_key(self):
        """Gets the entity_key of this Validation.  # noqa: E501

        Entity description.  # noqa: E501

        :return: The entity_key of this Validation.  # noqa: E501
        :rtype: str
        """
        return self._entity_key

    @entity_key.setter
    def entity_key(self, entity_key):
        """Sets the entity_key of this Validation.

        Entity description.  # noqa: E501

        :param entity_key: The entity_key of this Validation.  # noqa: E501
        :type entity_key: str
        """
        if (self.local_vars_configuration.client_side_validation and
                entity_key is not None and len(entity_key) > 1024):
            raise ValueError("Invalid value for `entity_key`, length must be less than or equal to `1024`")  # noqa: E501

        self._entity_key = entity_key

    @property
    def entity_type(self):
        """Gets the entity_type of this Validation.  # noqa: E501

        Entity type.  # noqa: E501

        :return: The entity_type of this Validation.  # noqa: E501
        :rtype: str
        """
        return self._entity_type

    @entity_type.setter
    def entity_type(self, entity_type):
        """Sets the entity_type of this Validation.

        Entity type.  # noqa: E501

        :param entity_type: The entity_type of this Validation.  # noqa: E501
        :type entity_type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                entity_type is not None and len(entity_type) > 1024):
            raise ValueError("Invalid value for `entity_type`, length must be less than or equal to `1024`")  # noqa: E501

        self._entity_type = entity_type

    @property
    def info(self):
        """Gets the info of this Validation.  # noqa: E501

        Information about validation.  # noqa: E501

        :return: The info of this Validation.  # noqa: E501
        :rtype: str
        """
        return self._info

    @info.setter
    def info(self, info):
        """Sets the info of this Validation.

        Information about validation.  # noqa: E501

        :param info: The info of this Validation.  # noqa: E501
        :type info: str
        """
        if self.local_vars_configuration.client_side_validation and info is None:  # noqa: E501
            raise ValueError("Invalid value for `info`, must not be `None`")  # noqa: E501

        self._info = info

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
        if not isinstance(other, Validation):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Validation):
            return True

        return self.to_dict() != other.to_dict()
