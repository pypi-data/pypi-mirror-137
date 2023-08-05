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


class TraceData(object):
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
        'code': 'str',
        'client': 'str',
        'server': 'str',
        'service': 'str',
        'method': 'str',
        'time': 'datetime'
    }

    attribute_map = {
        'code': 'code',
        'client': 'client',
        'server': 'server',
        'service': 'service',
        'method': 'method',
        'time': 'time'
    }

    def __init__(self, code=None, client=None, server=None, service=None, method=None, time=None, local_vars_configuration=None):  # noqa: E501
        """TraceData - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._code = None
        self._client = None
        self._server = None
        self._service = None
        self._method = None
        self._time = None
        self.discriminator = None

        self.code = code
        if client is not None:
            self.client = client
        if server is not None:
            self.server = server
        if service is not None:
            self.service = service
        if method is not None:
            self.method = method
        if time is not None:
            self.time = time

    @property
    def code(self):
        """Gets the code of this TraceData.  # noqa: E501

        Unique operation code.  # noqa: E501

        :return: The code of this TraceData.  # noqa: E501
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this TraceData.

        Unique operation code.  # noqa: E501

        :param code: The code of this TraceData.  # noqa: E501
        :type code: str
        """
        if self.local_vars_configuration.client_side_validation and code is None:  # noqa: E501
            raise ValueError("Invalid value for `code`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                code is not None and len(code) > 256):
            raise ValueError("Invalid value for `code`, length must be less than or equal to `256`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                code is not None and len(code) < 3):
            raise ValueError("Invalid value for `code`, length must be greater than or equal to `3`")  # noqa: E501

        self._code = code

    @property
    def client(self):
        """Gets the client of this TraceData.  # noqa: E501

        Client ID.  # noqa: E501

        :return: The client of this TraceData.  # noqa: E501
        :rtype: str
        """
        return self._client

    @client.setter
    def client(self, client):
        """Sets the client of this TraceData.

        Client ID.  # noqa: E501

        :param client: The client of this TraceData.  # noqa: E501
        :type client: str
        """
        if (self.local_vars_configuration.client_side_validation and
                client is not None and len(client) > 256):
            raise ValueError("Invalid value for `client`, length must be less than or equal to `256`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                client is not None and len(client) < 2):
            raise ValueError("Invalid value for `client`, length must be greater than or equal to `2`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                client is not None and not re.search(r'\w+', client)):  # noqa: E501
            raise ValueError(r"Invalid value for `client`, must be a follow pattern or equal to `/\w+/`")  # noqa: E501

        self._client = client

    @property
    def server(self):
        """Gets the server of this TraceData.  # noqa: E501

        Server ID.  # noqa: E501

        :return: The server of this TraceData.  # noqa: E501
        :rtype: str
        """
        return self._server

    @server.setter
    def server(self, server):
        """Sets the server of this TraceData.

        Server ID.  # noqa: E501

        :param server: The server of this TraceData.  # noqa: E501
        :type server: str
        """
        if (self.local_vars_configuration.client_side_validation and
                server is not None and len(server) > 256):
            raise ValueError("Invalid value for `server`, length must be less than or equal to `256`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                server is not None and len(server) < 2):
            raise ValueError("Invalid value for `server`, length must be greater than or equal to `2`")  # noqa: E501

        self._server = server

    @property
    def service(self):
        """Gets the service of this TraceData.  # noqa: E501

        Service name.  # noqa: E501

        :return: The service of this TraceData.  # noqa: E501
        :rtype: str
        """
        return self._service

    @service.setter
    def service(self, service):
        """Sets the service of this TraceData.

        Service name.  # noqa: E501

        :param service: The service of this TraceData.  # noqa: E501
        :type service: str
        """
        allowed_values = ["LASTMILE", "DELIVERY", "FIELDSERVICE", "MERCHANDISER", "ROUTING", "CLUSTERING", "ACCOUNT", "STOCK", "ADMIN"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and service not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `service` ({0}), must be one of {1}"  # noqa: E501
                .format(service, allowed_values)
            )

        self._service = service

    @property
    def method(self):
        """Gets the method of this TraceData.  # noqa: E501

        Method name.  # noqa: E501

        :return: The method of this TraceData.  # noqa: E501
        :rtype: str
        """
        return self._method

    @method.setter
    def method(self, method):
        """Sets the method of this TraceData.

        Method name.  # noqa: E501

        :param method: The method of this TraceData.  # noqa: E501
        :type method: str
        """
        allowed_values = ["PLAN", "REPLAN", "ACTUALIZE", "CONVERT", "ANALYTICS", "PREDICT", "VALIDATE", "ROUTE", "MATRIX", "CLUSTER"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and method not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `method` ({0}), must be one of {1}"  # noqa: E501
                .format(method, allowed_values)
            )

        self._method = method

    @property
    def time(self):
        """Gets the time of this TraceData.  # noqa: E501

        Date and time service method run in the [RFC 3339, section 5.6 (ISO8601)](https://tools.ietf.org/html/rfc3339#section-5.6) format.  # noqa: E501

        :return: The time of this TraceData.  # noqa: E501
        :rtype: datetime
        """
        return self._time

    @time.setter
    def time(self, time):
        """Sets the time of this TraceData.

        Date and time service method run in the [RFC 3339, section 5.6 (ISO8601)](https://tools.ietf.org/html/rfc3339#section-5.6) format.  # noqa: E501

        :param time: The time of this TraceData.  # noqa: E501
        :type time: datetime
        """

        self._time = time

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
        if not isinstance(other, TraceData):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TraceData):
            return True

        return self.to_dict() != other.to_dict()
