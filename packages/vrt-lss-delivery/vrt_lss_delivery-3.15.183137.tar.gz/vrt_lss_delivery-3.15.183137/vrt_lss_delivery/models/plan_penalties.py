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


class PlanPenalties(object):
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
        'compatibilities': 'list[CompatibilityPenalty]'
    }

    attribute_map = {
        'compatibilities': 'compatibilities'
    }

    def __init__(self, compatibilities=[], local_vars_configuration=None):  # noqa: E501
        """PlanPenalties - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._compatibilities = None
        self.discriminator = None

        if compatibilities is not None:
            self.compatibilities = compatibilities

    @property
    def compatibilities(self):
        """Gets the compatibilities of this PlanPenalties.  # noqa: E501

        Penalties for compatibility violation.  # noqa: E501

        :return: The compatibilities of this PlanPenalties.  # noqa: E501
        :rtype: list[CompatibilityPenalty]
        """
        return self._compatibilities

    @compatibilities.setter
    def compatibilities(self, compatibilities):
        """Sets the compatibilities of this PlanPenalties.

        Penalties for compatibility violation.  # noqa: E501

        :param compatibilities: The compatibilities of this PlanPenalties.  # noqa: E501
        :type compatibilities: list[CompatibilityPenalty]
        """
        if (self.local_vars_configuration.client_side_validation and
                compatibilities is not None and len(compatibilities) > 1000000):
            raise ValueError("Invalid value for `compatibilities`, number of items must be less than or equal to `1000000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                compatibilities is not None and len(compatibilities) < 0):
            raise ValueError("Invalid value for `compatibilities`, number of items must be greater than or equal to `0`")  # noqa: E501

        self._compatibilities = compatibilities

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
        if not isinstance(other, PlanPenalties):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PlanPenalties):
            return True

        return self.to_dict() != other.to_dict()
