# coding: utf-8

"""
    Veeroute.Account

    Veeroute Account Panel  # noqa: E501

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

from vrt_lss_account.configuration import Configuration


class MethodStatistics(object):
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
        'method': 'MethodName',
        'unique_points_per_day': 'int',
        'points_per_day': 'int'
    }

    attribute_map = {
        'method': 'method',
        'unique_points_per_day': 'unique_points_per_day',
        'points_per_day': 'points_per_day'
    }

    def __init__(self, method=None, unique_points_per_day=0, points_per_day=0, local_vars_configuration=None):  # noqa: E501
        """MethodStatistics - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._method = None
        self._unique_points_per_day = None
        self._points_per_day = None
        self.discriminator = None

        self.method = method
        self.unique_points_per_day = unique_points_per_day
        self.points_per_day = points_per_day

    @property
    def method(self):
        """Gets the method of this MethodStatistics.  # noqa: E501


        :return: The method of this MethodStatistics.  # noqa: E501
        :rtype: MethodName
        """
        return self._method

    @method.setter
    def method(self, method):
        """Sets the method of this MethodStatistics.


        :param method: The method of this MethodStatistics.  # noqa: E501
        :type method: MethodName
        """
        if self.local_vars_configuration.client_side_validation and method is None:  # noqa: E501
            raise ValueError("Invalid value for `method`, must not be `None`")  # noqa: E501

        self._method = method

    @property
    def unique_points_per_day(self):
        """Gets the unique_points_per_day of this MethodStatistics.  # noqa: E501

        Unique points per day.  # noqa: E501

        :return: The unique_points_per_day of this MethodStatistics.  # noqa: E501
        :rtype: int
        """
        return self._unique_points_per_day

    @unique_points_per_day.setter
    def unique_points_per_day(self, unique_points_per_day):
        """Sets the unique_points_per_day of this MethodStatistics.

        Unique points per day.  # noqa: E501

        :param unique_points_per_day: The unique_points_per_day of this MethodStatistics.  # noqa: E501
        :type unique_points_per_day: int
        """
        if self.local_vars_configuration.client_side_validation and unique_points_per_day is None:  # noqa: E501
            raise ValueError("Invalid value for `unique_points_per_day`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                unique_points_per_day is not None and unique_points_per_day > 10000000):  # noqa: E501
            raise ValueError("Invalid value for `unique_points_per_day`, must be a value less than or equal to `10000000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                unique_points_per_day is not None and unique_points_per_day < 0):  # noqa: E501
            raise ValueError("Invalid value for `unique_points_per_day`, must be a value greater than or equal to `0`")  # noqa: E501

        self._unique_points_per_day = unique_points_per_day

    @property
    def points_per_day(self):
        """Gets the points_per_day of this MethodStatistics.  # noqa: E501

        Non-unique points per day.  # noqa: E501

        :return: The points_per_day of this MethodStatistics.  # noqa: E501
        :rtype: int
        """
        return self._points_per_day

    @points_per_day.setter
    def points_per_day(self, points_per_day):
        """Sets the points_per_day of this MethodStatistics.

        Non-unique points per day.  # noqa: E501

        :param points_per_day: The points_per_day of this MethodStatistics.  # noqa: E501
        :type points_per_day: int
        """
        if self.local_vars_configuration.client_side_validation and points_per_day is None:  # noqa: E501
            raise ValueError("Invalid value for `points_per_day`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                points_per_day is not None and points_per_day > 10000000):  # noqa: E501
            raise ValueError("Invalid value for `points_per_day`, must be a value less than or equal to `10000000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                points_per_day is not None and points_per_day < 0):  # noqa: E501
            raise ValueError("Invalid value for `points_per_day`, must be a value greater than or equal to `0`")  # noqa: E501

        self._points_per_day = points_per_day

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
        if not isinstance(other, MethodStatistics):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, MethodStatistics):
            return True

        return self.to_dict() != other.to_dict()
