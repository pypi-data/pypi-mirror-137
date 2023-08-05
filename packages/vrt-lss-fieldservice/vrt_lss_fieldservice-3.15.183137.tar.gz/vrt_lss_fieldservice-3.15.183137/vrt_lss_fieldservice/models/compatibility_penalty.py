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


class CompatibilityPenalty(object):
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
        'tag': 'str',
        'penalty': 'float'
    }

    attribute_map = {
        'tag': 'tag',
        'penalty': 'penalty'
    }

    def __init__(self, tag=None, penalty=0, local_vars_configuration=None):  # noqa: E501
        """CompatibilityPenalty - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._tag = None
        self._penalty = None
        self.discriminator = None

        self.tag = tag
        self.penalty = penalty

    @property
    def tag(self):
        """Gets the tag of this CompatibilityPenalty.  # noqa: E501

        Tag from list of [compatibilities](https://docs.veeroute.ru/#/lss/lastmile?id=compatibilities).   # noqa: E501

        :return: The tag of this CompatibilityPenalty.  # noqa: E501
        :rtype: str
        """
        return self._tag

    @tag.setter
    def tag(self, tag):
        """Sets the tag of this CompatibilityPenalty.

        Tag from list of [compatibilities](https://docs.veeroute.ru/#/lss/lastmile?id=compatibilities).   # noqa: E501

        :param tag: The tag of this CompatibilityPenalty.  # noqa: E501
        :type tag: str
        """
        if self.local_vars_configuration.client_side_validation and tag is None:  # noqa: E501
            raise ValueError("Invalid value for `tag`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                tag is not None and len(tag) > 256):
            raise ValueError("Invalid value for `tag`, length must be less than or equal to `256`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                tag is not None and len(tag) < 1):
            raise ValueError("Invalid value for `tag`, length must be greater than or equal to `1`")  # noqa: E501

        self._tag = tag

    @property
    def penalty(self):
        """Gets the penalty of this CompatibilityPenalty.  # noqa: E501

        Penalty for violation of compatibility for the specified tag.   # noqa: E501

        :return: The penalty of this CompatibilityPenalty.  # noqa: E501
        :rtype: float
        """
        return self._penalty

    @penalty.setter
    def penalty(self, penalty):
        """Sets the penalty of this CompatibilityPenalty.

        Penalty for violation of compatibility for the specified tag.   # noqa: E501

        :param penalty: The penalty of this CompatibilityPenalty.  # noqa: E501
        :type penalty: float
        """
        if self.local_vars_configuration.client_side_validation and penalty is None:  # noqa: E501
            raise ValueError("Invalid value for `penalty`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                penalty is not None and penalty > 1000000):  # noqa: E501
            raise ValueError("Invalid value for `penalty`, must be a value less than or equal to `1000000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                penalty is not None and penalty < 0):  # noqa: E501
            raise ValueError("Invalid value for `penalty`, must be a value greater than or equal to `0`")  # noqa: E501

        self._penalty = penalty

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
        if not isinstance(other, CompatibilityPenalty):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CompatibilityPenalty):
            return True

        return self.to_dict() != other.to_dict()
