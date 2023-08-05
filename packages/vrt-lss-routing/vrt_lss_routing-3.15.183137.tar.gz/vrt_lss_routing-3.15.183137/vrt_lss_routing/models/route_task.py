# coding: utf-8

"""
    Veeroute.Routing

    Veeroute Routing API  # noqa: E501

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

from vrt_lss_routing.configuration import Configuration


class RouteTask(object):
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
        'waypoints': 'list[Waypoint]',
        'transport_type': 'TransportType',
        'toll_roads': 'bool',
        'ferry_crossing': 'bool',
        'departure_time': 'datetime',
        'result_timezone': 'int',
        'geo_provider': 'str',
        'detail': 'bool',
        'full_segments': 'bool',
        'polyline': 'bool'
    }

    attribute_map = {
        'waypoints': 'waypoints',
        'transport_type': 'transport_type',
        'toll_roads': 'toll_roads',
        'ferry_crossing': 'ferry_crossing',
        'departure_time': 'departure_time',
        'result_timezone': 'result_timezone',
        'geo_provider': 'geo_provider',
        'detail': 'detail',
        'full_segments': 'full_segments',
        'polyline': 'polyline'
    }

    def __init__(self, waypoints=None, transport_type=None, toll_roads=True, ferry_crossing=True, departure_time=None, result_timezone=0, geo_provider=None, detail=False, full_segments=True, polyline=True, local_vars_configuration=None):  # noqa: E501
        """RouteTask - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._waypoints = None
        self._transport_type = None
        self._toll_roads = None
        self._ferry_crossing = None
        self._departure_time = None
        self._result_timezone = None
        self._geo_provider = None
        self._detail = None
        self._full_segments = None
        self._polyline = None
        self.discriminator = None

        self.waypoints = waypoints
        if transport_type is not None:
            self.transport_type = transport_type
        if toll_roads is not None:
            self.toll_roads = toll_roads
        if ferry_crossing is not None:
            self.ferry_crossing = ferry_crossing
        if departure_time is not None:
            self.departure_time = departure_time
        if result_timezone is not None:
            self.result_timezone = result_timezone
        if geo_provider is not None:
            self.geo_provider = geo_provider
        if detail is not None:
            self.detail = detail
        if full_segments is not None:
            self.full_segments = full_segments
        if polyline is not None:
            self.polyline = polyline

    @property
    def waypoints(self):
        """Gets the waypoints of this RouteTask.  # noqa: E501

        Array of geographical points to build path between them.  # noqa: E501

        :return: The waypoints of this RouteTask.  # noqa: E501
        :rtype: list[Waypoint]
        """
        return self._waypoints

    @waypoints.setter
    def waypoints(self, waypoints):
        """Sets the waypoints of this RouteTask.

        Array of geographical points to build path between them.  # noqa: E501

        :param waypoints: The waypoints of this RouteTask.  # noqa: E501
        :type waypoints: list[Waypoint]
        """
        if self.local_vars_configuration.client_side_validation and waypoints is None:  # noqa: E501
            raise ValueError("Invalid value for `waypoints`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                waypoints is not None and len(waypoints) > 9000):
            raise ValueError("Invalid value for `waypoints`, number of items must be less than or equal to `9000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                waypoints is not None and len(waypoints) < 2):
            raise ValueError("Invalid value for `waypoints`, number of items must be greater than or equal to `2`")  # noqa: E501

        self._waypoints = waypoints

    @property
    def transport_type(self):
        """Gets the transport_type of this RouteTask.  # noqa: E501


        :return: The transport_type of this RouteTask.  # noqa: E501
        :rtype: TransportType
        """
        return self._transport_type

    @transport_type.setter
    def transport_type(self, transport_type):
        """Sets the transport_type of this RouteTask.


        :param transport_type: The transport_type of this RouteTask.  # noqa: E501
        :type transport_type: TransportType
        """

        self._transport_type = transport_type

    @property
    def toll_roads(self):
        """Gets the toll_roads of this RouteTask.  # noqa: E501

        Use toll roads.  # noqa: E501

        :return: The toll_roads of this RouteTask.  # noqa: E501
        :rtype: bool
        """
        return self._toll_roads

    @toll_roads.setter
    def toll_roads(self, toll_roads):
        """Sets the toll_roads of this RouteTask.

        Use toll roads.  # noqa: E501

        :param toll_roads: The toll_roads of this RouteTask.  # noqa: E501
        :type toll_roads: bool
        """

        self._toll_roads = toll_roads

    @property
    def ferry_crossing(self):
        """Gets the ferry_crossing of this RouteTask.  # noqa: E501

        Use ferry crossing.  # noqa: E501

        :return: The ferry_crossing of this RouteTask.  # noqa: E501
        :rtype: bool
        """
        return self._ferry_crossing

    @ferry_crossing.setter
    def ferry_crossing(self, ferry_crossing):
        """Sets the ferry_crossing of this RouteTask.

        Use ferry crossing.  # noqa: E501

        :param ferry_crossing: The ferry_crossing of this RouteTask.  # noqa: E501
        :type ferry_crossing: bool
        """

        self._ferry_crossing = ferry_crossing

    @property
    def departure_time(self):
        """Gets the departure_time of this RouteTask.  # noqa: E501

        Departure date and time according to the [RFC 3339, section 5.6 (ISO8601)](https://tools.ietf.org/html/rfc3339#section-5.6).  # noqa: E501

        :return: The departure_time of this RouteTask.  # noqa: E501
        :rtype: datetime
        """
        return self._departure_time

    @departure_time.setter
    def departure_time(self, departure_time):
        """Sets the departure_time of this RouteTask.

        Departure date and time according to the [RFC 3339, section 5.6 (ISO8601)](https://tools.ietf.org/html/rfc3339#section-5.6).  # noqa: E501

        :param departure_time: The departure_time of this RouteTask.  # noqa: E501
        :type departure_time: datetime
        """

        self._departure_time = departure_time

    @property
    def result_timezone(self):
        """Gets the result_timezone of this RouteTask.  # noqa: E501

        Time zone for calculation results.  # noqa: E501

        :return: The result_timezone of this RouteTask.  # noqa: E501
        :rtype: int
        """
        return self._result_timezone

    @result_timezone.setter
    def result_timezone(self, result_timezone):
        """Sets the result_timezone of this RouteTask.

        Time zone for calculation results.  # noqa: E501

        :param result_timezone: The result_timezone of this RouteTask.  # noqa: E501
        :type result_timezone: int
        """
        if (self.local_vars_configuration.client_side_validation and
                result_timezone is not None and result_timezone > 12):  # noqa: E501
            raise ValueError("Invalid value for `result_timezone`, must be a value less than or equal to `12`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                result_timezone is not None and result_timezone < -12):  # noqa: E501
            raise ValueError("Invalid value for `result_timezone`, must be a value greater than or equal to `-12`")  # noqa: E501

        self._result_timezone = result_timezone

    @property
    def geo_provider(self):
        """Gets the geo_provider of this RouteTask.  # noqa: E501

        Geodata provider.  # noqa: E501

        :return: The geo_provider of this RouteTask.  # noqa: E501
        :rtype: str
        """
        return self._geo_provider

    @geo_provider.setter
    def geo_provider(self, geo_provider):
        """Sets the geo_provider of this RouteTask.

        Geodata provider.  # noqa: E501

        :param geo_provider: The geo_provider of this RouteTask.  # noqa: E501
        :type geo_provider: str
        """
        if (self.local_vars_configuration.client_side_validation and
                geo_provider is not None and len(geo_provider) > 256):
            raise ValueError("Invalid value for `geo_provider`, length must be less than or equal to `256`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                geo_provider is not None and len(geo_provider) < 1):
            raise ValueError("Invalid value for `geo_provider`, length must be greater than or equal to `1`")  # noqa: E501

        self._geo_provider = geo_provider

    @property
    def detail(self):
        """Gets the detail of this RouteTask.  # noqa: E501

        Planning a detailed route.  # noqa: E501

        :return: The detail of this RouteTask.  # noqa: E501
        :rtype: bool
        """
        return self._detail

    @detail.setter
    def detail(self, detail):
        """Sets the detail of this RouteTask.

        Planning a detailed route.  # noqa: E501

        :param detail: The detail of this RouteTask.  # noqa: E501
        :type detail: bool
        """

        self._detail = detail

    @property
    def full_segments(self):
        """Gets the full_segments of this RouteTask.  # noqa: E501

        Return full segments list.  # noqa: E501

        :return: The full_segments of this RouteTask.  # noqa: E501
        :rtype: bool
        """
        return self._full_segments

    @full_segments.setter
    def full_segments(self, full_segments):
        """Sets the full_segments of this RouteTask.

        Return full segments list.  # noqa: E501

        :param full_segments: The full_segments of this RouteTask.  # noqa: E501
        :type full_segments: bool
        """

        self._full_segments = full_segments

    @property
    def polyline(self):
        """Gets the polyline of this RouteTask.  # noqa: E501

        Generate a polyline between points.  # noqa: E501

        :return: The polyline of this RouteTask.  # noqa: E501
        :rtype: bool
        """
        return self._polyline

    @polyline.setter
    def polyline(self, polyline):
        """Sets the polyline of this RouteTask.

        Generate a polyline between points.  # noqa: E501

        :param polyline: The polyline of this RouteTask.  # noqa: E501
        :type polyline: bool
        """

        self._polyline = polyline

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
        if not isinstance(other, RouteTask):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, RouteTask):
            return True

        return self.to_dict() != other.to_dict()
