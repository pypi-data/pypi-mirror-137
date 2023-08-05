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


class StopStatistics(object):
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
        'location': 'Location',
        'location_key': 'str',
        'demand_ids': 'list[str]',
        'measurements': 'Measurements',
        'upload': 'TransportLoad',
        'download': 'TransportLoad',
        'current_load': 'TransportLoad'
    }

    attribute_map = {
        'location': 'location',
        'location_key': 'location_key',
        'demand_ids': 'demand_ids',
        'measurements': 'measurements',
        'upload': 'upload',
        'download': 'download',
        'current_load': 'current_load'
    }

    def __init__(self, location=None, location_key=None, demand_ids=None, measurements=None, upload=None, download=None, current_load=None, local_vars_configuration=None):  # noqa: E501
        """StopStatistics - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._location = None
        self._location_key = None
        self._demand_ids = None
        self._measurements = None
        self._upload = None
        self._download = None
        self._current_load = None
        self.discriminator = None

        self.location = location
        if location_key is not None:
            self.location_key = location_key
        if demand_ids is not None:
            self.demand_ids = demand_ids
        self.measurements = measurements
        self.upload = upload
        self.download = download
        self.current_load = current_load

    @property
    def location(self):
        """Gets the location of this StopStatistics.  # noqa: E501


        :return: The location of this StopStatistics.  # noqa: E501
        :rtype: Location
        """
        return self._location

    @location.setter
    def location(self, location):
        """Sets the location of this StopStatistics.


        :param location: The location of this StopStatistics.  # noqa: E501
        :type location: Location
        """
        if self.local_vars_configuration.client_side_validation and location is None:  # noqa: E501
            raise ValueError("Invalid value for `location`, must not be `None`")  # noqa: E501

        self._location = location

    @property
    def location_key(self):
        """Gets the location_key of this StopStatistics.  # noqa: E501

        Location key to separate different locations with the same geographical coordinates.  # noqa: E501

        :return: The location_key of this StopStatistics.  # noqa: E501
        :rtype: str
        """
        return self._location_key

    @location_key.setter
    def location_key(self, location_key):
        """Sets the location_key of this StopStatistics.

        Location key to separate different locations with the same geographical coordinates.  # noqa: E501

        :param location_key: The location_key of this StopStatistics.  # noqa: E501
        :type location_key: str
        """
        if (self.local_vars_configuration.client_side_validation and
                location_key is not None and len(location_key) > 1024):
            raise ValueError("Invalid value for `location_key`, length must be less than or equal to `1024`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                location_key is not None and len(location_key) < 1):
            raise ValueError("Invalid value for `location_key`, length must be greater than or equal to `1`")  # noqa: E501

        self._location_key = location_key

    @property
    def demand_ids(self):
        """Gets the demand_ids of this StopStatistics.  # noqa: E501

        ID list of demands fulfilled at this stop.  # noqa: E501

        :return: The demand_ids of this StopStatistics.  # noqa: E501
        :rtype: list[str]
        """
        return self._demand_ids

    @demand_ids.setter
    def demand_ids(self, demand_ids):
        """Sets the demand_ids of this StopStatistics.

        ID list of demands fulfilled at this stop.  # noqa: E501

        :param demand_ids: The demand_ids of this StopStatistics.  # noqa: E501
        :type demand_ids: list[str]
        """

        self._demand_ids = demand_ids

    @property
    def measurements(self):
        """Gets the measurements of this StopStatistics.  # noqa: E501


        :return: The measurements of this StopStatistics.  # noqa: E501
        :rtype: Measurements
        """
        return self._measurements

    @measurements.setter
    def measurements(self, measurements):
        """Sets the measurements of this StopStatistics.


        :param measurements: The measurements of this StopStatistics.  # noqa: E501
        :type measurements: Measurements
        """

        self._measurements = measurements

    @property
    def upload(self):
        """Gets the upload of this StopStatistics.  # noqa: E501


        :return: The upload of this StopStatistics.  # noqa: E501
        :rtype: TransportLoad
        """
        return self._upload

    @upload.setter
    def upload(self, upload):
        """Sets the upload of this StopStatistics.


        :param upload: The upload of this StopStatistics.  # noqa: E501
        :type upload: TransportLoad
        """

        self._upload = upload

    @property
    def download(self):
        """Gets the download of this StopStatistics.  # noqa: E501


        :return: The download of this StopStatistics.  # noqa: E501
        :rtype: TransportLoad
        """
        return self._download

    @download.setter
    def download(self, download):
        """Sets the download of this StopStatistics.


        :param download: The download of this StopStatistics.  # noqa: E501
        :type download: TransportLoad
        """

        self._download = download

    @property
    def current_load(self):
        """Gets the current_load of this StopStatistics.  # noqa: E501


        :return: The current_load of this StopStatistics.  # noqa: E501
        :rtype: TransportLoad
        """
        return self._current_load

    @current_load.setter
    def current_load(self, current_load):
        """Sets the current_load of this StopStatistics.


        :param current_load: The current_load of this StopStatistics.  # noqa: E501
        :type current_load: TransportLoad
        """

        self._current_load = current_load

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
        if not isinstance(other, StopStatistics):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, StopStatistics):
            return True

        return self.to_dict() != other.to_dict()
