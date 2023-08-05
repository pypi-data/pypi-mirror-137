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


class CostPenalty(object):
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
        'start_time': 'datetime',
        'period': 'int',
        'value': 'float',
        'max_value': 'float'
    }

    attribute_map = {
        'start_time': 'start_time',
        'period': 'period',
        'value': 'value',
        'max_value': 'max_value'
    }

    def __init__(self, start_time=None, period=60, value=0, max_value=0, local_vars_configuration=None):  # noqa: E501
        """CostPenalty - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._start_time = None
        self._period = None
        self._value = None
        self._max_value = None
        self.discriminator = None

        self.start_time = start_time
        self.period = period
        self.value = value
        self.max_value = max_value

    @property
    def start_time(self):
        """Gets the start_time of this CostPenalty.  # noqa: E501

        Time in the [RFC 3339, section 5.6 (ISO8601)](https://tools.ietf.org/html/rfc3339#section-5.6) format, since the penalty takes effect.  # noqa: E501

        :return: The start_time of this CostPenalty.  # noqa: E501
        :rtype: datetime
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this CostPenalty.

        Time in the [RFC 3339, section 5.6 (ISO8601)](https://tools.ietf.org/html/rfc3339#section-5.6) format, since the penalty takes effect.  # noqa: E501

        :param start_time: The start_time of this CostPenalty.  # noqa: E501
        :type start_time: datetime
        """
        if self.local_vars_configuration.client_side_validation and start_time is None:  # noqa: E501
            raise ValueError("Invalid value for `start_time`, must not be `None`")  # noqa: E501

        self._start_time = start_time

    @property
    def period(self):
        """Gets the period of this CostPenalty.  # noqa: E501

        The period in minutes after which the penalty amount increases by `value`.  # noqa: E501

        :return: The period of this CostPenalty.  # noqa: E501
        :rtype: int
        """
        return self._period

    @period.setter
    def period(self, period):
        """Sets the period of this CostPenalty.

        The period in minutes after which the penalty amount increases by `value`.  # noqa: E501

        :param period: The period of this CostPenalty.  # noqa: E501
        :type period: int
        """
        if self.local_vars_configuration.client_side_validation and period is None:  # noqa: E501
            raise ValueError("Invalid value for `period`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                period is not None and period > 1440):  # noqa: E501
            raise ValueError("Invalid value for `period`, must be a value less than or equal to `1440`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                period is not None and period < 1):  # noqa: E501
            raise ValueError("Invalid value for `period`, must be a value greater than or equal to `1`")  # noqa: E501

        self._period = period

    @property
    def value(self):
        """Gets the value of this CostPenalty.  # noqa: E501

        The cost by which the penalty is increased each `period`.  # noqa: E501

        :return: The value of this CostPenalty.  # noqa: E501
        :rtype: float
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this CostPenalty.

        The cost by which the penalty is increased each `period`.  # noqa: E501

        :param value: The value of this CostPenalty.  # noqa: E501
        :type value: float
        """
        if self.local_vars_configuration.client_side_validation and value is None:  # noqa: E501
            raise ValueError("Invalid value for `value`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                value is not None and value > 1000000):  # noqa: E501
            raise ValueError("Invalid value for `value`, must be a value less than or equal to `1000000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                value is not None and value < 0):  # noqa: E501
            raise ValueError("Invalid value for `value`, must be a value greater than or equal to `0`")  # noqa: E501

        self._value = value

    @property
    def max_value(self):
        """Gets the max_value of this CostPenalty.  # noqa: E501

        The maximum possible penalty value.  # noqa: E501

        :return: The max_value of this CostPenalty.  # noqa: E501
        :rtype: float
        """
        return self._max_value

    @max_value.setter
    def max_value(self, max_value):
        """Sets the max_value of this CostPenalty.

        The maximum possible penalty value.  # noqa: E501

        :param max_value: The max_value of this CostPenalty.  # noqa: E501
        :type max_value: float
        """
        if self.local_vars_configuration.client_side_validation and max_value is None:  # noqa: E501
            raise ValueError("Invalid value for `max_value`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                max_value is not None and max_value > 1000000):  # noqa: E501
            raise ValueError("Invalid value for `max_value`, must be a value less than or equal to `1000000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                max_value is not None and max_value < 0):  # noqa: E501
            raise ValueError("Invalid value for `max_value`, must be a value greater than or equal to `0`")  # noqa: E501

        self._max_value = max_value

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
        if not isinstance(other, CostPenalty):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CostPenalty):
            return True

        return self.to_dict() != other.to_dict()
