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


class Measurements(object):
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
        'driving_time': 'int',
        'waiting_time': 'int',
        'working_time': 'int',
        'arriving_time': 'int',
        'departure_time': 'int',
        'total_time': 'int',
        'distance': 'int',
        'time_window': 'TimeWindow'
    }

    attribute_map = {
        'driving_time': 'driving_time',
        'waiting_time': 'waiting_time',
        'working_time': 'working_time',
        'arriving_time': 'arriving_time',
        'departure_time': 'departure_time',
        'total_time': 'total_time',
        'distance': 'distance',
        'time_window': 'time_window'
    }

    def __init__(self, driving_time=None, waiting_time=None, working_time=None, arriving_time=None, departure_time=None, total_time=None, distance=None, time_window=None, local_vars_configuration=None):  # noqa: E501
        """Measurements - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._driving_time = None
        self._waiting_time = None
        self._working_time = None
        self._arriving_time = None
        self._departure_time = None
        self._total_time = None
        self._distance = None
        self._time_window = None
        self.discriminator = None

        self.driving_time = driving_time
        self.waiting_time = waiting_time
        self.working_time = working_time
        self.arriving_time = arriving_time
        self.departure_time = departure_time
        self.total_time = total_time
        self.distance = distance
        if time_window is not None:
            self.time_window = time_window

    @property
    def driving_time(self):
        """Gets the driving_time of this Measurements.  # noqa: E501

        Driving time, in minutes. For a stop, the driving time from the previous stop to the current location.   # noqa: E501

        :return: The driving_time of this Measurements.  # noqa: E501
        :rtype: int
        """
        return self._driving_time

    @driving_time.setter
    def driving_time(self, driving_time):
        """Sets the driving_time of this Measurements.

        Driving time, in minutes. For a stop, the driving time from the previous stop to the current location.   # noqa: E501

        :param driving_time: The driving_time of this Measurements.  # noqa: E501
        :type driving_time: int
        """
        if self.local_vars_configuration.client_side_validation and driving_time is None:  # noqa: E501
            raise ValueError("Invalid value for `driving_time`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                driving_time is not None and driving_time < 0):  # noqa: E501
            raise ValueError("Invalid value for `driving_time`, must be a value greater than or equal to `0`")  # noqa: E501

        self._driving_time = driving_time

    @property
    def waiting_time(self):
        """Gets the waiting_time of this Measurements.  # noqa: E501

        Total waiting time for all locations, in minutes. For a stop, the waiting time for work to be completed at the location, in minutes.   # noqa: E501

        :return: The waiting_time of this Measurements.  # noqa: E501
        :rtype: int
        """
        return self._waiting_time

    @waiting_time.setter
    def waiting_time(self, waiting_time):
        """Sets the waiting_time of this Measurements.

        Total waiting time for all locations, in minutes. For a stop, the waiting time for work to be completed at the location, in minutes.   # noqa: E501

        :param waiting_time: The waiting_time of this Measurements.  # noqa: E501
        :type waiting_time: int
        """
        if self.local_vars_configuration.client_side_validation and waiting_time is None:  # noqa: E501
            raise ValueError("Invalid value for `waiting_time`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                waiting_time is not None and waiting_time < 0):  # noqa: E501
            raise ValueError("Invalid value for `waiting_time`, must be a value greater than or equal to `0`")  # noqa: E501

        self._waiting_time = waiting_time

    @property
    def working_time(self):
        """Gets the working_time of this Measurements.  # noqa: E501

        The total work completion time at all locations assigned to the trip. For a stop - the time spent on actual work completion at the location.   # noqa: E501

        :return: The working_time of this Measurements.  # noqa: E501
        :rtype: int
        """
        return self._working_time

    @working_time.setter
    def working_time(self, working_time):
        """Sets the working_time of this Measurements.

        The total work completion time at all locations assigned to the trip. For a stop - the time spent on actual work completion at the location.   # noqa: E501

        :param working_time: The working_time of this Measurements.  # noqa: E501
        :type working_time: int
        """
        if self.local_vars_configuration.client_side_validation and working_time is None:  # noqa: E501
            raise ValueError("Invalid value for `working_time`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                working_time is not None and working_time < 0):  # noqa: E501
            raise ValueError("Invalid value for `working_time`, must be a value greater than or equal to `0`")  # noqa: E501

        self._working_time = working_time

    @property
    def arriving_time(self):
        """Gets the arriving_time of this Measurements.  # noqa: E501

        Total time spent on driving up/parking at the locations, in minutes. For a stop - the time spent on driving up/parking at the location.   # noqa: E501

        :return: The arriving_time of this Measurements.  # noqa: E501
        :rtype: int
        """
        return self._arriving_time

    @arriving_time.setter
    def arriving_time(self, arriving_time):
        """Sets the arriving_time of this Measurements.

        Total time spent on driving up/parking at the locations, in minutes. For a stop - the time spent on driving up/parking at the location.   # noqa: E501

        :param arriving_time: The arriving_time of this Measurements.  # noqa: E501
        :type arriving_time: int
        """
        if self.local_vars_configuration.client_side_validation and arriving_time is None:  # noqa: E501
            raise ValueError("Invalid value for `arriving_time`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                arriving_time is not None and arriving_time < 0):  # noqa: E501
            raise ValueError("Invalid value for `arriving_time`, must be a value greater than or equal to `0`")  # noqa: E501

        self._arriving_time = arriving_time

    @property
    def departure_time(self):
        """Gets the departure_time of this Measurements.  # noqa: E501

        Total time to leave the locations. For a stop - the time spent on departure from the location.   # noqa: E501

        :return: The departure_time of this Measurements.  # noqa: E501
        :rtype: int
        """
        return self._departure_time

    @departure_time.setter
    def departure_time(self, departure_time):
        """Sets the departure_time of this Measurements.

        Total time to leave the locations. For a stop - the time spent on departure from the location.   # noqa: E501

        :param departure_time: The departure_time of this Measurements.  # noqa: E501
        :type departure_time: int
        """
        if self.local_vars_configuration.client_side_validation and departure_time is None:  # noqa: E501
            raise ValueError("Invalid value for `departure_time`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                departure_time is not None and departure_time < 0):  # noqa: E501
            raise ValueError("Invalid value for `departure_time`, must be a value greater than or equal to `0`")  # noqa: E501

        self._departure_time = departure_time

    @property
    def total_time(self):
        """Gets the total_time of this Measurements.  # noqa: E501

        Total stop/trip time/total number of trips, in minutes.        It consists of `driving_time` + `waiting_time` + `working_time` + `arriving_time` + `departure_time`.    # noqa: E501

        :return: The total_time of this Measurements.  # noqa: E501
        :rtype: int
        """
        return self._total_time

    @total_time.setter
    def total_time(self, total_time):
        """Sets the total_time of this Measurements.

        Total stop/trip time/total number of trips, in minutes.        It consists of `driving_time` + `waiting_time` + `working_time` + `arriving_time` + `departure_time`.    # noqa: E501

        :param total_time: The total_time of this Measurements.  # noqa: E501
        :type total_time: int
        """
        if self.local_vars_configuration.client_side_validation and total_time is None:  # noqa: E501
            raise ValueError("Invalid value for `total_time`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                total_time is not None and total_time < 0):  # noqa: E501
            raise ValueError("Invalid value for `total_time`, must be a value greater than or equal to `0`")  # noqa: E501

        self._total_time = total_time

    @property
    def distance(self):
        """Gets the distance of this Measurements.  # noqa: E501

        The total length of the trip / set of trips, in meters. For a stop, the distance from the previous stop to the current location.   # noqa: E501

        :return: The distance of this Measurements.  # noqa: E501
        :rtype: int
        """
        return self._distance

    @distance.setter
    def distance(self, distance):
        """Sets the distance of this Measurements.

        The total length of the trip / set of trips, in meters. For a stop, the distance from the previous stop to the current location.   # noqa: E501

        :param distance: The distance of this Measurements.  # noqa: E501
        :type distance: int
        """
        if self.local_vars_configuration.client_side_validation and distance is None:  # noqa: E501
            raise ValueError("Invalid value for `distance`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                distance is not None and distance < 0):  # noqa: E501
            raise ValueError("Invalid value for `distance`, must be a value greater than or equal to `0`")  # noqa: E501

        self._distance = distance

    @property
    def time_window(self):
        """Gets the time_window of this Measurements.  # noqa: E501


        :return: The time_window of this Measurements.  # noqa: E501
        :rtype: TimeWindow
        """
        return self._time_window

    @time_window.setter
    def time_window(self, time_window):
        """Sets the time_window of this Measurements.


        :param time_window: The time_window of this Measurements.  # noqa: E501
        :type time_window: TimeWindow
        """

        self._time_window = time_window

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
        if not isinstance(other, Measurements):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Measurements):
            return True

        return self.to_dict() != other.to_dict()
