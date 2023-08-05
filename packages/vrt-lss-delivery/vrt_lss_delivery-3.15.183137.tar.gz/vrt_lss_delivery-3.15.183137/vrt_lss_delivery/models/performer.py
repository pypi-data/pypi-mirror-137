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


class Performer(object):
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
        'key': 'str',
        'count': 'int',
        'box': 'Box',
        'start_location': 'Location',
        'finish_location': 'Location',
        'features': 'list[str]',
        'transport_type': 'TransportType',
        'shifts': 'list[Shift]',
        'tariff': 'Tariff'
    }

    attribute_map = {
        'key': 'key',
        'count': 'count',
        'box': 'box',
        'start_location': 'start_location',
        'finish_location': 'finish_location',
        'features': 'features',
        'transport_type': 'transport_type',
        'shifts': 'shifts',
        'tariff': 'tariff'
    }

    def __init__(self, key=None, count=1, box=None, start_location=None, finish_location=None, features=[], transport_type=None, shifts=None, tariff=None, local_vars_configuration=None):  # noqa: E501
        """Performer - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._key = None
        self._count = None
        self._box = None
        self._start_location = None
        self._finish_location = None
        self._features = None
        self._transport_type = None
        self._shifts = None
        self._tariff = None
        self.discriminator = None

        self.key = key
        if count is not None:
            self.count = count
        self.box = box
        if start_location is not None:
            self.start_location = start_location
        if finish_location is not None:
            self.finish_location = finish_location
        if features is not None:
            self.features = features
        if transport_type is not None:
            self.transport_type = transport_type
        self.shifts = shifts
        if tariff is not None:
            self.tariff = tariff

    @property
    def key(self):
        """Gets the key of this Performer.  # noqa: E501

        Unique ID.  # noqa: E501

        :return: The key of this Performer.  # noqa: E501
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """Sets the key of this Performer.

        Unique ID.  # noqa: E501

        :param key: The key of this Performer.  # noqa: E501
        :type key: str
        """
        if self.local_vars_configuration.client_side_validation and key is None:  # noqa: E501
            raise ValueError("Invalid value for `key`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                key is not None and len(key) > 1024):
            raise ValueError("Invalid value for `key`, length must be less than or equal to `1024`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                key is not None and len(key) < 1):
            raise ValueError("Invalid value for `key`, length must be greater than or equal to `1`")  # noqa: E501

        self._key = key

    @property
    def count(self):
        """Gets the count of this Performer.  # noqa: E501

        Number of equal performers in this group.  # noqa: E501

        :return: The count of this Performer.  # noqa: E501
        :rtype: int
        """
        return self._count

    @count.setter
    def count(self, count):
        """Sets the count of this Performer.

        Number of equal performers in this group.  # noqa: E501

        :param count: The count of this Performer.  # noqa: E501
        :type count: int
        """
        if (self.local_vars_configuration.client_side_validation and
                count is not None and count > 5000):  # noqa: E501
            raise ValueError("Invalid value for `count`, must be a value less than or equal to `5000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                count is not None and count < 1):  # noqa: E501
            raise ValueError("Invalid value for `count`, must be a value greater than or equal to `1`")  # noqa: E501

        self._count = count

    @property
    def box(self):
        """Gets the box of this Performer.  # noqa: E501


        :return: The box of this Performer.  # noqa: E501
        :rtype: Box
        """
        return self._box

    @box.setter
    def box(self, box):
        """Sets the box of this Performer.


        :param box: The box of this Performer.  # noqa: E501
        :type box: Box
        """

        self._box = box

    @property
    def start_location(self):
        """Gets the start_location of this Performer.  # noqa: E501


        :return: The start_location of this Performer.  # noqa: E501
        :rtype: Location
        """
        return self._start_location

    @start_location.setter
    def start_location(self, start_location):
        """Sets the start_location of this Performer.


        :param start_location: The start_location of this Performer.  # noqa: E501
        :type start_location: Location
        """

        self._start_location = start_location

    @property
    def finish_location(self):
        """Gets the finish_location of this Performer.  # noqa: E501


        :return: The finish_location of this Performer.  # noqa: E501
        :rtype: Location
        """
        return self._finish_location

    @finish_location.setter
    def finish_location(self, finish_location):
        """Sets the finish_location of this Performer.


        :param finish_location: The finish_location of this Performer.  # noqa: E501
        :type finish_location: Location
        """

        self._finish_location = finish_location

    @property
    def features(self):
        """Gets the features of this Performer.  # noqa: E501

        Performer's features list. Used to check whether the performer is compatible with orders.   # noqa: E501

        :return: The features of this Performer.  # noqa: E501
        :rtype: list[str]
        """
        return self._features

    @features.setter
    def features(self, features):
        """Sets the features of this Performer.

        Performer's features list. Used to check whether the performer is compatible with orders.   # noqa: E501

        :param features: The features of this Performer.  # noqa: E501
        :type features: list[str]
        """
        if (self.local_vars_configuration.client_side_validation and
                features is not None and len(features) > 1000):
            raise ValueError("Invalid value for `features`, number of items must be less than or equal to `1000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                features is not None and len(features) < 0):
            raise ValueError("Invalid value for `features`, number of items must be greater than or equal to `0`")  # noqa: E501

        self._features = features

    @property
    def transport_type(self):
        """Gets the transport_type of this Performer.  # noqa: E501


        :return: The transport_type of this Performer.  # noqa: E501
        :rtype: TransportType
        """
        return self._transport_type

    @transport_type.setter
    def transport_type(self, transport_type):
        """Sets the transport_type of this Performer.


        :param transport_type: The transport_type of this Performer.  # noqa: E501
        :type transport_type: TransportType
        """

        self._transport_type = transport_type

    @property
    def shifts(self):
        """Gets the shifts of this Performer.  # noqa: E501

        List of performer's shifts.  # noqa: E501

        :return: The shifts of this Performer.  # noqa: E501
        :rtype: list[Shift]
        """
        return self._shifts

    @shifts.setter
    def shifts(self, shifts):
        """Sets the shifts of this Performer.

        List of performer's shifts.  # noqa: E501

        :param shifts: The shifts of this Performer.  # noqa: E501
        :type shifts: list[Shift]
        """
        if self.local_vars_configuration.client_side_validation and shifts is None:  # noqa: E501
            raise ValueError("Invalid value for `shifts`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                shifts is not None and len(shifts) > 100):
            raise ValueError("Invalid value for `shifts`, number of items must be less than or equal to `100`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                shifts is not None and len(shifts) < 1):
            raise ValueError("Invalid value for `shifts`, number of items must be greater than or equal to `1`")  # noqa: E501

        self._shifts = shifts

    @property
    def tariff(self):
        """Gets the tariff of this Performer.  # noqa: E501


        :return: The tariff of this Performer.  # noqa: E501
        :rtype: Tariff
        """
        return self._tariff

    @tariff.setter
    def tariff(self, tariff):
        """Sets the tariff of this Performer.


        :param tariff: The tariff of this Performer.  # noqa: E501
        :type tariff: Tariff
        """

        self._tariff = tariff

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
        if not isinstance(other, Performer):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Performer):
            return True

        return self.to_dict() != other.to_dict()
