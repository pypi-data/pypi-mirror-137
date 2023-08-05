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


class DateStatistics(object):
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
        'date': 'date',
        'services': 'list[ServiceStatistics]'
    }

    attribute_map = {
        'date': 'date',
        'services': 'services'
    }

    def __init__(self, date=None, services=None, local_vars_configuration=None):  # noqa: E501
        """DateStatistics - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._date = None
        self._services = None
        self.discriminator = None

        self.date = date
        self.services = services

    @property
    def date(self):
        """Gets the date of this DateStatistics.  # noqa: E501

        Date in the YYYY-MM-DD format.  # noqa: E501

        :return: The date of this DateStatistics.  # noqa: E501
        :rtype: date
        """
        return self._date

    @date.setter
    def date(self, date):
        """Sets the date of this DateStatistics.

        Date in the YYYY-MM-DD format.  # noqa: E501

        :param date: The date of this DateStatistics.  # noqa: E501
        :type date: date
        """
        if self.local_vars_configuration.client_side_validation and date is None:  # noqa: E501
            raise ValueError("Invalid value for `date`, must not be `None`")  # noqa: E501

        self._date = date

    @property
    def services(self):
        """Gets the services of this DateStatistics.  # noqa: E501

        Statistics list for each service on the specified date.  # noqa: E501

        :return: The services of this DateStatistics.  # noqa: E501
        :rtype: list[ServiceStatistics]
        """
        return self._services

    @services.setter
    def services(self, services):
        """Sets the services of this DateStatistics.

        Statistics list for each service on the specified date.  # noqa: E501

        :param services: The services of this DateStatistics.  # noqa: E501
        :type services: list[ServiceStatistics]
        """
        if self.local_vars_configuration.client_side_validation and services is None:  # noqa: E501
            raise ValueError("Invalid value for `services`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                services is not None and len(services) < 1):
            raise ValueError("Invalid value for `services`, number of items must be greater than or equal to `1`")  # noqa: E501

        self._services = services

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
        if not isinstance(other, DateStatistics):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DateStatistics):
            return True

        return self.to_dict() != other.to_dict()
