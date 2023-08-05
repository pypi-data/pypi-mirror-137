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


class RouteStep(object):
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
        'transport_type': 'TransportType',
        'polyline': 'RoutePolyline'
    }

    attribute_map = {
        'transport_type': 'transport_type',
        'polyline': 'polyline'
    }

    def __init__(self, transport_type=None, polyline=None, local_vars_configuration=None):  # noqa: E501
        """RouteStep - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._transport_type = None
        self._polyline = None
        self.discriminator = None

        if transport_type is not None:
            self.transport_type = transport_type
        if polyline is not None:
            self.polyline = polyline

    @property
    def transport_type(self):
        """Gets the transport_type of this RouteStep.  # noqa: E501


        :return: The transport_type of this RouteStep.  # noqa: E501
        :rtype: TransportType
        """
        return self._transport_type

    @transport_type.setter
    def transport_type(self, transport_type):
        """Sets the transport_type of this RouteStep.


        :param transport_type: The transport_type of this RouteStep.  # noqa: E501
        :type transport_type: TransportType
        """

        self._transport_type = transport_type

    @property
    def polyline(self):
        """Gets the polyline of this RouteStep.  # noqa: E501


        :return: The polyline of this RouteStep.  # noqa: E501
        :rtype: RoutePolyline
        """
        return self._polyline

    @polyline.setter
    def polyline(self, polyline):
        """Sets the polyline of this RouteStep.


        :param polyline: The polyline of this RouteStep.  # noqa: E501
        :type polyline: RoutePolyline
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
        if not isinstance(other, RouteStep):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, RouteStep):
            return True

        return self.to_dict() != other.to_dict()
