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


class AccountAction(object):
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
        'time': 'datetime',
        'service': 'ServiceName',
        'method': 'MethodName',
        'detail': 'UserActionDetail'
    }

    attribute_map = {
        'time': 'time',
        'service': 'service',
        'method': 'method',
        'detail': 'detail'
    }

    def __init__(self, time=None, service=None, method=None, detail=None, local_vars_configuration=None):  # noqa: E501
        """AccountAction - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._time = None
        self._service = None
        self._method = None
        self._detail = None
        self.discriminator = None

        self.time = time
        self.service = service
        self.method = method
        self.detail = detail

    @property
    def time(self):
        """Gets the time of this AccountAction.  # noqa: E501

        Data and time in the [RFC 3339, section 5.6 (ISO8601)](https://tools.ietf.org/html/rfc3339#section-5.6) format.  # noqa: E501

        :return: The time of this AccountAction.  # noqa: E501
        :rtype: datetime
        """
        return self._time

    @time.setter
    def time(self, time):
        """Sets the time of this AccountAction.

        Data and time in the [RFC 3339, section 5.6 (ISO8601)](https://tools.ietf.org/html/rfc3339#section-5.6) format.  # noqa: E501

        :param time: The time of this AccountAction.  # noqa: E501
        :type time: datetime
        """
        if self.local_vars_configuration.client_side_validation and time is None:  # noqa: E501
            raise ValueError("Invalid value for `time`, must not be `None`")  # noqa: E501

        self._time = time

    @property
    def service(self):
        """Gets the service of this AccountAction.  # noqa: E501


        :return: The service of this AccountAction.  # noqa: E501
        :rtype: ServiceName
        """
        return self._service

    @service.setter
    def service(self, service):
        """Sets the service of this AccountAction.


        :param service: The service of this AccountAction.  # noqa: E501
        :type service: ServiceName
        """
        if self.local_vars_configuration.client_side_validation and service is None:  # noqa: E501
            raise ValueError("Invalid value for `service`, must not be `None`")  # noqa: E501

        self._service = service

    @property
    def method(self):
        """Gets the method of this AccountAction.  # noqa: E501


        :return: The method of this AccountAction.  # noqa: E501
        :rtype: MethodName
        """
        return self._method

    @method.setter
    def method(self, method):
        """Sets the method of this AccountAction.


        :param method: The method of this AccountAction.  # noqa: E501
        :type method: MethodName
        """
        if self.local_vars_configuration.client_side_validation and method is None:  # noqa: E501
            raise ValueError("Invalid value for `method`, must not be `None`")  # noqa: E501

        self._method = method

    @property
    def detail(self):
        """Gets the detail of this AccountAction.  # noqa: E501


        :return: The detail of this AccountAction.  # noqa: E501
        :rtype: UserActionDetail
        """
        return self._detail

    @detail.setter
    def detail(self, detail):
        """Sets the detail of this AccountAction.


        :param detail: The detail of this AccountAction.  # noqa: E501
        :type detail: UserActionDetail
        """
        if self.local_vars_configuration.client_side_validation and detail is None:  # noqa: E501
            raise ValueError("Invalid value for `detail`, must not be `None`")  # noqa: E501

        self._detail = detail

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
        if not isinstance(other, AccountAction):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AccountAction):
            return True

        return self.to_dict() != other.to_dict()
