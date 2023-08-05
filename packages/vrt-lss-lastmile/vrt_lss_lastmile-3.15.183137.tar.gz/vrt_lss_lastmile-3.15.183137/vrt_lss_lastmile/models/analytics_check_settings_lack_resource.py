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


class AnalyticsCheckSettingsLackResource(object):
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
        'percent': 'int'
    }

    attribute_map = {
        'percent': 'percent'
    }

    def __init__(self, percent=90, local_vars_configuration=None):  # noqa: E501
        """AnalyticsCheckSettingsLackResource - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._percent = None
        self.discriminator = None

        if percent is not None:
            self.percent = percent

    @property
    def percent(self):
        """Gets the percent of this AnalyticsCheckSettingsLackResource.  # noqa: E501

        Percent.  # noqa: E501

        :return: The percent of this AnalyticsCheckSettingsLackResource.  # noqa: E501
        :rtype: int
        """
        return self._percent

    @percent.setter
    def percent(self, percent):
        """Sets the percent of this AnalyticsCheckSettingsLackResource.

        Percent.  # noqa: E501

        :param percent: The percent of this AnalyticsCheckSettingsLackResource.  # noqa: E501
        :type percent: int
        """
        if (self.local_vars_configuration.client_side_validation and
                percent is not None and percent > 100):  # noqa: E501
            raise ValueError("Invalid value for `percent`, must be a value less than or equal to `100`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                percent is not None and percent < 0):  # noqa: E501
            raise ValueError("Invalid value for `percent`, must be a value greater than or equal to `0`")  # noqa: E501

        self._percent = percent

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
        if not isinstance(other, AnalyticsCheckSettingsLackResource):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AnalyticsCheckSettingsLackResource):
            return True

        return self.to_dict() != other.to_dict()
