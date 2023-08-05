# coding: utf-8

"""
    Veeroute.Fieldservice

    Veeroute Field Service Engineers API  # noqa: E501

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

from vrt_lss_fieldservice.configuration import Configuration


class ObjectsMetrics(object):
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
        'keys': 'list[str]',
        'count': 'int'
    }

    attribute_map = {
        'keys': 'keys',
        'count': 'count'
    }

    def __init__(self, keys=None, count=None, local_vars_configuration=None):  # noqa: E501
        """ObjectsMetrics - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._keys = None
        self._count = None
        self.discriminator = None

        if keys is not None:
            self.keys = keys
        if count is not None:
            self.count = count

    @property
    def keys(self):
        """Gets the keys of this ObjectsMetrics.  # noqa: E501

        List of object's keys.  # noqa: E501

        :return: The keys of this ObjectsMetrics.  # noqa: E501
        :rtype: list[str]
        """
        return self._keys

    @keys.setter
    def keys(self, keys):
        """Sets the keys of this ObjectsMetrics.

        List of object's keys.  # noqa: E501

        :param keys: The keys of this ObjectsMetrics.  # noqa: E501
        :type keys: list[str]
        """
        if (self.local_vars_configuration.client_side_validation and
                keys is not None and len(keys) > 9000):
            raise ValueError("Invalid value for `keys`, number of items must be less than or equal to `9000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                keys is not None and len(keys) < 0):
            raise ValueError("Invalid value for `keys`, number of items must be greater than or equal to `0`")  # noqa: E501

        self._keys = keys

    @property
    def count(self):
        """Gets the count of this ObjectsMetrics.  # noqa: E501

        The total number of objects.  # noqa: E501

        :return: The count of this ObjectsMetrics.  # noqa: E501
        :rtype: int
        """
        return self._count

    @count.setter
    def count(self, count):
        """Sets the count of this ObjectsMetrics.

        The total number of objects.  # noqa: E501

        :param count: The count of this ObjectsMetrics.  # noqa: E501
        :type count: int
        """
        if (self.local_vars_configuration.client_side_validation and
                count is not None and count > 9000):  # noqa: E501
            raise ValueError("Invalid value for `count`, must be a value less than or equal to `9000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                count is not None and count < 0):  # noqa: E501
            raise ValueError("Invalid value for `count`, must be a value greater than or equal to `0`")  # noqa: E501

        self._count = count

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
        if not isinstance(other, ObjectsMetrics):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ObjectsMetrics):
            return True

        return self.to_dict() != other.to_dict()
