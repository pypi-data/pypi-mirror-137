# coding: utf-8

"""
    Veeroute.Merchandiser

    Veeroute Merchandiser API  # noqa: E501

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

from vrt_lss_merchandiser.configuration import Configuration


class Capacity(object):
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
        'mass': 'float',
        'volume': 'float',
        'capacity_x': 'float',
        'capacity_y': 'float',
        'capacity_z': 'float'
    }

    attribute_map = {
        'mass': 'mass',
        'volume': 'volume',
        'capacity_x': 'capacity_x',
        'capacity_y': 'capacity_y',
        'capacity_z': 'capacity_z'
    }

    def __init__(self, mass=0, volume=0, capacity_x=0, capacity_y=0, capacity_z=0, local_vars_configuration=None):  # noqa: E501
        """Capacity - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._mass = None
        self._volume = None
        self._capacity_x = None
        self._capacity_y = None
        self._capacity_z = None
        self.discriminator = None

        if mass is not None:
            self.mass = mass
        if volume is not None:
            self.volume = volume
        if capacity_x is not None:
            self.capacity_x = capacity_x
        if capacity_y is not None:
            self.capacity_y = capacity_y
        if capacity_z is not None:
            self.capacity_z = capacity_z

    @property
    def mass(self):
        """Gets the mass of this Capacity.  # noqa: E501

        Weight in kilograms.  # noqa: E501

        :return: The mass of this Capacity.  # noqa: E501
        :rtype: float
        """
        return self._mass

    @mass.setter
    def mass(self, mass):
        """Sets the mass of this Capacity.

        Weight in kilograms.  # noqa: E501

        :param mass: The mass of this Capacity.  # noqa: E501
        :type mass: float
        """
        if (self.local_vars_configuration.client_side_validation and
                mass is not None and mass > 1000000):  # noqa: E501
            raise ValueError("Invalid value for `mass`, must be a value less than or equal to `1000000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                mass is not None and mass < 0):  # noqa: E501
            raise ValueError("Invalid value for `mass`, must be a value greater than or equal to `0`")  # noqa: E501

        self._mass = mass

    @property
    def volume(self):
        """Gets the volume of this Capacity.  # noqa: E501

        Volume in cubic meters.  # noqa: E501

        :return: The volume of this Capacity.  # noqa: E501
        :rtype: float
        """
        return self._volume

    @volume.setter
    def volume(self, volume):
        """Sets the volume of this Capacity.

        Volume in cubic meters.  # noqa: E501

        :param volume: The volume of this Capacity.  # noqa: E501
        :type volume: float
        """
        if (self.local_vars_configuration.client_side_validation and
                volume is not None and volume > 1000000):  # noqa: E501
            raise ValueError("Invalid value for `volume`, must be a value less than or equal to `1000000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                volume is not None and volume < 0):  # noqa: E501
            raise ValueError("Invalid value for `volume`, must be a value greater than or equal to `0`")  # noqa: E501

        self._volume = volume

    @property
    def capacity_x(self):
        """Gets the capacity_x of this Capacity.  # noqa: E501

        Additional capacity parameter (X) for measuring cargoes and compartments in alternative units. For example, to account for cargo in pieces (this parameter is equal to one for a cargo and the maximum number of cargo to hold for a compartment).   # noqa: E501

        :return: The capacity_x of this Capacity.  # noqa: E501
        :rtype: float
        """
        return self._capacity_x

    @capacity_x.setter
    def capacity_x(self, capacity_x):
        """Sets the capacity_x of this Capacity.

        Additional capacity parameter (X) for measuring cargoes and compartments in alternative units. For example, to account for cargo in pieces (this parameter is equal to one for a cargo and the maximum number of cargo to hold for a compartment).   # noqa: E501

        :param capacity_x: The capacity_x of this Capacity.  # noqa: E501
        :type capacity_x: float
        """
        if (self.local_vars_configuration.client_side_validation and
                capacity_x is not None and capacity_x > 1000000):  # noqa: E501
            raise ValueError("Invalid value for `capacity_x`, must be a value less than or equal to `1000000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                capacity_x is not None and capacity_x < 0):  # noqa: E501
            raise ValueError("Invalid value for `capacity_x`, must be a value greater than or equal to `0`")  # noqa: E501

        self._capacity_x = capacity_x

    @property
    def capacity_y(self):
        """Gets the capacity_y of this Capacity.  # noqa: E501

        Additional capacity parameter (Y) for measuring cargoes and compartments in alternative units.  # noqa: E501

        :return: The capacity_y of this Capacity.  # noqa: E501
        :rtype: float
        """
        return self._capacity_y

    @capacity_y.setter
    def capacity_y(self, capacity_y):
        """Sets the capacity_y of this Capacity.

        Additional capacity parameter (Y) for measuring cargoes and compartments in alternative units.  # noqa: E501

        :param capacity_y: The capacity_y of this Capacity.  # noqa: E501
        :type capacity_y: float
        """
        if (self.local_vars_configuration.client_side_validation and
                capacity_y is not None and capacity_y > 1000000):  # noqa: E501
            raise ValueError("Invalid value for `capacity_y`, must be a value less than or equal to `1000000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                capacity_y is not None and capacity_y < 0):  # noqa: E501
            raise ValueError("Invalid value for `capacity_y`, must be a value greater than or equal to `0`")  # noqa: E501

        self._capacity_y = capacity_y

    @property
    def capacity_z(self):
        """Gets the capacity_z of this Capacity.  # noqa: E501

        Additional capacity parameter (Z) for measuring cargoes and compartments in alternative units.  # noqa: E501

        :return: The capacity_z of this Capacity.  # noqa: E501
        :rtype: float
        """
        return self._capacity_z

    @capacity_z.setter
    def capacity_z(self, capacity_z):
        """Sets the capacity_z of this Capacity.

        Additional capacity parameter (Z) for measuring cargoes and compartments in alternative units.  # noqa: E501

        :param capacity_z: The capacity_z of this Capacity.  # noqa: E501
        :type capacity_z: float
        """
        if (self.local_vars_configuration.client_side_validation and
                capacity_z is not None and capacity_z > 1000000):  # noqa: E501
            raise ValueError("Invalid value for `capacity_z`, must be a value less than or equal to `1000000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                capacity_z is not None and capacity_z < 0):  # noqa: E501
            raise ValueError("Invalid value for `capacity_z`, must be a value greater than or equal to `0`")  # noqa: E501

        self._capacity_z = capacity_z

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
        if not isinstance(other, Capacity):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Capacity):
            return True

        return self.to_dict() != other.to_dict()
