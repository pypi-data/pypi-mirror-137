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


class UserReportFilter(object):
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
        'date_window': 'DateWindow'
    }

    attribute_map = {
        'name': 'name',
        'date_window': 'date_window'
    }

    def __init__(self, name='UsageReport', date_window=None, local_vars_configuration=None):  # noqa: E501
        """UserReportFilter - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._date_window = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if date_window is not None:
            self.date_window = date_window

    @property
    def name(self):
        """Gets the name of this UserReportFilter.  # noqa: E501

        Report type.  # noqa: E501

        :return: The name of this UserReportFilter.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this UserReportFilter.

        Report type.  # noqa: E501

        :param name: The name of this UserReportFilter.  # noqa: E501
        :type name: str
        """
        allowed_values = ["UsageReport"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and name not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `name` ({0}), must be one of {1}"  # noqa: E501
                .format(name, allowed_values)
            )

        self._name = name

    @property
    def date_window(self):
        """Gets the date_window of this UserReportFilter.  # noqa: E501


        :return: The date_window of this UserReportFilter.  # noqa: E501
        :rtype: DateWindow
        """
        return self._date_window

    @date_window.setter
    def date_window(self, date_window):
        """Sets the date_window of this UserReportFilter.


        :param date_window: The date_window of this UserReportFilter.  # noqa: E501
        :type date_window: DateWindow
        """

        self._date_window = date_window

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
        if not isinstance(other, UserReportFilter):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UserReportFilter):
            return True

        return self.to_dict() != other.to_dict()
