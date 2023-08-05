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


class Waypoint(object):
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
        'name': 'str',
        'latitude': 'float',
        'longitude': 'float',
        'duration': 'int'
    }

    attribute_map = {
        'name': 'name',
        'latitude': 'latitude',
        'longitude': 'longitude',
        'duration': 'duration'
    }

    def __init__(self, name=None, latitude=None, longitude=None, duration=0, local_vars_configuration=None):  # noqa: E501
        """Waypoint - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._latitude = None
        self._longitude = None
        self._duration = None
        self.discriminator = None

        if name is not None:
            self.name = name
        self.latitude = latitude
        self.longitude = longitude
        if duration is not None:
            self.duration = duration

    @property
    def name(self):
        """Gets the name of this Waypoint.  # noqa: E501

        Name of the point.  # noqa: E501

        :return: The name of this Waypoint.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Waypoint.

        Name of the point.  # noqa: E501

        :param name: The name of this Waypoint.  # noqa: E501
        :type name: str
        """
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) > 1024):
            raise ValueError("Invalid value for `name`, length must be less than or equal to `1024`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) < 0):
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `0`")  # noqa: E501

        self._name = name

    @property
    def latitude(self):
        """Gets the latitude of this Waypoint.  # noqa: E501

        Latitude in degrees.  # noqa: E501

        :return: The latitude of this Waypoint.  # noqa: E501
        :rtype: float
        """
        return self._latitude

    @latitude.setter
    def latitude(self, latitude):
        """Sets the latitude of this Waypoint.

        Latitude in degrees.  # noqa: E501

        :param latitude: The latitude of this Waypoint.  # noqa: E501
        :type latitude: float
        """
        if self.local_vars_configuration.client_side_validation and latitude is None:  # noqa: E501
            raise ValueError("Invalid value for `latitude`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                latitude is not None and latitude > 90):  # noqa: E501
            raise ValueError("Invalid value for `latitude`, must be a value less than or equal to `90`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                latitude is not None and latitude < -90):  # noqa: E501
            raise ValueError("Invalid value for `latitude`, must be a value greater than or equal to `-90`")  # noqa: E501

        self._latitude = latitude

    @property
    def longitude(self):
        """Gets the longitude of this Waypoint.  # noqa: E501

        Longitude in degrees.  # noqa: E501

        :return: The longitude of this Waypoint.  # noqa: E501
        :rtype: float
        """
        return self._longitude

    @longitude.setter
    def longitude(self, longitude):
        """Sets the longitude of this Waypoint.

        Longitude in degrees.  # noqa: E501

        :param longitude: The longitude of this Waypoint.  # noqa: E501
        :type longitude: float
        """
        if self.local_vars_configuration.client_side_validation and longitude is None:  # noqa: E501
            raise ValueError("Invalid value for `longitude`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                longitude is not None and longitude > 180):  # noqa: E501
            raise ValueError("Invalid value for `longitude`, must be a value less than or equal to `180`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                longitude is not None and longitude < -180):  # noqa: E501
            raise ValueError("Invalid value for `longitude`, must be a value greater than or equal to `-180`")  # noqa: E501

        self._longitude = longitude

    @property
    def duration(self):
        """Gets the duration of this Waypoint.  # noqa: E501

        Stop time at the point, in minutes.  # noqa: E501

        :return: The duration of this Waypoint.  # noqa: E501
        :rtype: int
        """
        return self._duration

    @duration.setter
    def duration(self, duration):
        """Sets the duration of this Waypoint.

        Stop time at the point, in minutes.  # noqa: E501

        :param duration: The duration of this Waypoint.  # noqa: E501
        :type duration: int
        """
        if (self.local_vars_configuration.client_side_validation and
                duration is not None and duration > 43800):  # noqa: E501
            raise ValueError("Invalid value for `duration`, must be a value less than or equal to `43800`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                duration is not None and duration < 0):  # noqa: E501
            raise ValueError("Invalid value for `duration`, must be a value greater than or equal to `0`")  # noqa: E501

        self._duration = duration

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
        if not isinstance(other, Waypoint):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Waypoint):
            return True

        return self.to_dict() != other.to_dict()
