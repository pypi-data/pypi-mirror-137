# coding: utf-8

"""
    Veeroute.Delivery

    Veeroute Delivery API  # noqa: E501

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

from vrt_lss_delivery.configuration import Configuration


class ConvertSettings(object):
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
        'route_index_from': 'int',
        'route_index_to': 'int'
    }

    attribute_map = {
        'route_index_from': 'route_index_from',
        'route_index_to': 'route_index_to'
    }

    def __init__(self, route_index_from=1, route_index_to=10000, local_vars_configuration=None):  # noqa: E501
        """ConvertSettings - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._route_index_from = None
        self._route_index_to = None
        self.discriminator = None

        if route_index_from is not None:
            self.route_index_from = route_index_from
        if route_index_to is not None:
            self.route_index_to = route_index_to

    @property
    def route_index_from(self):
        """Gets the route_index_from of this ConvertSettings.  # noqa: E501

        Route number to start the conversion. If not specified - the conversion starts from the 1st route.   # noqa: E501

        :return: The route_index_from of this ConvertSettings.  # noqa: E501
        :rtype: int
        """
        return self._route_index_from

    @route_index_from.setter
    def route_index_from(self, route_index_from):
        """Sets the route_index_from of this ConvertSettings.

        Route number to start the conversion. If not specified - the conversion starts from the 1st route.   # noqa: E501

        :param route_index_from: The route_index_from of this ConvertSettings.  # noqa: E501
        :type route_index_from: int
        """
        if (self.local_vars_configuration.client_side_validation and
                route_index_from is not None and route_index_from > 10000):  # noqa: E501
            raise ValueError("Invalid value for `route_index_from`, must be a value less than or equal to `10000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                route_index_from is not None and route_index_from < 1):  # noqa: E501
            raise ValueError("Invalid value for `route_index_from`, must be a value greater than or equal to `1`")  # noqa: E501

        self._route_index_from = route_index_from

    @property
    def route_index_to(self):
        """Gets the route_index_to of this ConvertSettings.  # noqa: E501

        Route number to finish the conversion. If not specified - the conversion finishes on the last route.   # noqa: E501

        :return: The route_index_to of this ConvertSettings.  # noqa: E501
        :rtype: int
        """
        return self._route_index_to

    @route_index_to.setter
    def route_index_to(self, route_index_to):
        """Sets the route_index_to of this ConvertSettings.

        Route number to finish the conversion. If not specified - the conversion finishes on the last route.   # noqa: E501

        :param route_index_to: The route_index_to of this ConvertSettings.  # noqa: E501
        :type route_index_to: int
        """
        if (self.local_vars_configuration.client_side_validation and
                route_index_to is not None and route_index_to > 10000):  # noqa: E501
            raise ValueError("Invalid value for `route_index_to`, must be a value less than or equal to `10000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                route_index_to is not None and route_index_to < 1):  # noqa: E501
            raise ValueError("Invalid value for `route_index_to`, must be a value greater than or equal to `1`")  # noqa: E501

        self._route_index_to = route_index_to

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
        if not isinstance(other, ConvertSettings):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ConvertSettings):
            return True

        return self.to_dict() != other.to_dict()
