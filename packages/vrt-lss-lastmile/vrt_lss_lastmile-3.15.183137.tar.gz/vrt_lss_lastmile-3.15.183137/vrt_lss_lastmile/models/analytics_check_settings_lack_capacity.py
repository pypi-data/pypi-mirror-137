# coding: utf-8

"""
    Veeroute.Lastmile

    Veeroute Lastmile API  # noqa: E501

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

from vrt_lss_lastmile.configuration import Configuration


class AnalyticsCheckSettingsLackCapacity(object):
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
        'max_ratio': 'int'
    }

    attribute_map = {
        'max_ratio': 'max_ratio'
    }

    def __init__(self, max_ratio=25, local_vars_configuration=None):  # noqa: E501
        """AnalyticsCheckSettingsLackCapacity - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._max_ratio = None
        self.discriminator = None

        if max_ratio is not None:
            self.max_ratio = max_ratio

    @property
    def max_ratio(self):
        """Gets the max_ratio of this AnalyticsCheckSettingsLackCapacity.  # noqa: E501

        Count.  # noqa: E501

        :return: The max_ratio of this AnalyticsCheckSettingsLackCapacity.  # noqa: E501
        :rtype: int
        """
        return self._max_ratio

    @max_ratio.setter
    def max_ratio(self, max_ratio):
        """Sets the max_ratio of this AnalyticsCheckSettingsLackCapacity.

        Count.  # noqa: E501

        :param max_ratio: The max_ratio of this AnalyticsCheckSettingsLackCapacity.  # noqa: E501
        :type max_ratio: int
        """
        if (self.local_vars_configuration.client_side_validation and
                max_ratio is not None and max_ratio > 1000):  # noqa: E501
            raise ValueError("Invalid value for `max_ratio`, must be a value less than or equal to `1000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                max_ratio is not None and max_ratio < 0):  # noqa: E501
            raise ValueError("Invalid value for `max_ratio`, must be a value greater than or equal to `0`")  # noqa: E501

        self._max_ratio = max_ratio

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
        if not isinstance(other, AnalyticsCheckSettingsLackCapacity):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AnalyticsCheckSettingsLackCapacity):
            return True

        return self.to_dict() != other.to_dict()
