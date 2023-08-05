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


class VersionResult(object):
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
        'major': 'int',
        'minor': 'int',
        'build': 'int'
    }

    attribute_map = {
        'major': 'major',
        'minor': 'minor',
        'build': 'build'
    }

    def __init__(self, major=None, minor=None, build=None, local_vars_configuration=None):  # noqa: E501
        """VersionResult - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._major = None
        self._minor = None
        self._build = None
        self.discriminator = None

        self.major = major
        self.minor = minor
        self.build = build

    @property
    def major(self):
        """Gets the major of this VersionResult.  # noqa: E501

        Major version. Contains incompatible API changes.   # noqa: E501

        :return: The major of this VersionResult.  # noqa: E501
        :rtype: int
        """
        return self._major

    @major.setter
    def major(self, major):
        """Sets the major of this VersionResult.

        Major version. Contains incompatible API changes.   # noqa: E501

        :param major: The major of this VersionResult.  # noqa: E501
        :type major: int
        """
        if self.local_vars_configuration.client_side_validation and major is None:  # noqa: E501
            raise ValueError("Invalid value for `major`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                major is not None and major > 100):  # noqa: E501
            raise ValueError("Invalid value for `major`, must be a value less than or equal to `100`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                major is not None and major < 0):  # noqa: E501
            raise ValueError("Invalid value for `major`, must be a value greater than or equal to `0`")  # noqa: E501

        self._major = major

    @property
    def minor(self):
        """Gets the minor of this VersionResult.  # noqa: E501

        Minor version. Contains new functionality in a backwards compatible manner.   # noqa: E501

        :return: The minor of this VersionResult.  # noqa: E501
        :rtype: int
        """
        return self._minor

    @minor.setter
    def minor(self, minor):
        """Sets the minor of this VersionResult.

        Minor version. Contains new functionality in a backwards compatible manner.   # noqa: E501

        :param minor: The minor of this VersionResult.  # noqa: E501
        :type minor: int
        """
        if self.local_vars_configuration.client_side_validation and minor is None:  # noqa: E501
            raise ValueError("Invalid value for `minor`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                minor is not None and minor > 100):  # noqa: E501
            raise ValueError("Invalid value for `minor`, must be a value less than or equal to `100`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                minor is not None and minor < 0):  # noqa: E501
            raise ValueError("Invalid value for `minor`, must be a value greater than or equal to `0`")  # noqa: E501

        self._minor = minor

    @property
    def build(self):
        """Gets the build of this VersionResult.  # noqa: E501

        Build version. Contains backwards compatible bug fixes and docs update.   # noqa: E501

        :return: The build of this VersionResult.  # noqa: E501
        :rtype: int
        """
        return self._build

    @build.setter
    def build(self, build):
        """Sets the build of this VersionResult.

        Build version. Contains backwards compatible bug fixes and docs update.   # noqa: E501

        :param build: The build of this VersionResult.  # noqa: E501
        :type build: int
        """
        if self.local_vars_configuration.client_side_validation and build is None:  # noqa: E501
            raise ValueError("Invalid value for `build`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                build is not None and build > 1000000):  # noqa: E501
            raise ValueError("Invalid value for `build`, must be a value less than or equal to `1000000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                build is not None and build < 0):  # noqa: E501
            raise ValueError("Invalid value for `build`, must be a value greater than or equal to `0`")  # noqa: E501

        self._build = build

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
        if not isinstance(other, VersionResult):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, VersionResult):
            return True

        return self.to_dict() != other.to_dict()
