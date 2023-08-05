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


class OrderAction(object):
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
        'order': 'Order',
        'order_time': 'TimeWindow',
        'location_time': 'TimeWindow'
    }

    attribute_map = {
        'order': 'order',
        'order_time': 'order_time',
        'location_time': 'location_time'
    }

    def __init__(self, order=None, order_time=None, location_time=None, local_vars_configuration=None):  # noqa: E501
        """OrderAction - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._order = None
        self._order_time = None
        self._location_time = None
        self.discriminator = None

        self.order = order
        self.order_time = order_time
        self.location_time = location_time

    @property
    def order(self):
        """Gets the order of this OrderAction.  # noqa: E501


        :return: The order of this OrderAction.  # noqa: E501
        :rtype: Order
        """
        return self._order

    @order.setter
    def order(self, order):
        """Sets the order of this OrderAction.


        :param order: The order of this OrderAction.  # noqa: E501
        :type order: Order
        """
        if self.local_vars_configuration.client_side_validation and order is None:  # noqa: E501
            raise ValueError("Invalid value for `order`, must not be `None`")  # noqa: E501

        self._order = order

    @property
    def order_time(self):
        """Gets the order_time of this OrderAction.  # noqa: E501


        :return: The order_time of this OrderAction.  # noqa: E501
        :rtype: TimeWindow
        """
        return self._order_time

    @order_time.setter
    def order_time(self, order_time):
        """Sets the order_time of this OrderAction.


        :param order_time: The order_time of this OrderAction.  # noqa: E501
        :type order_time: TimeWindow
        """
        if self.local_vars_configuration.client_side_validation and order_time is None:  # noqa: E501
            raise ValueError("Invalid value for `order_time`, must not be `None`")  # noqa: E501

        self._order_time = order_time

    @property
    def location_time(self):
        """Gets the location_time of this OrderAction.  # noqa: E501


        :return: The location_time of this OrderAction.  # noqa: E501
        :rtype: TimeWindow
        """
        return self._location_time

    @location_time.setter
    def location_time(self, location_time):
        """Sets the location_time of this OrderAction.


        :param location_time: The location_time of this OrderAction.  # noqa: E501
        :type location_time: TimeWindow
        """
        if self.local_vars_configuration.client_side_validation and location_time is None:  # noqa: E501
            raise ValueError("Invalid value for `location_time`, must not be `None`")  # noqa: E501

        self._location_time = location_time

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
        if not isinstance(other, OrderAction):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OrderAction):
            return True

        return self.to_dict() != other.to_dict()
