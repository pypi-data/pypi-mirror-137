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


class TimeWindowViolation(object):
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
        'before': 'ObjectsMetrics',
        'after': 'ObjectsMetrics'
    }

    attribute_map = {
        'before': 'before',
        'after': 'after'
    }

    def __init__(self, before=None, after=None, local_vars_configuration=None):  # noqa: E501
        """TimeWindowViolation - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._before = None
        self._after = None
        self.discriminator = None

        self.before = before
        self.after = after

    @property
    def before(self):
        """Gets the before of this TimeWindowViolation.  # noqa: E501


        :return: The before of this TimeWindowViolation.  # noqa: E501
        :rtype: ObjectsMetrics
        """
        return self._before

    @before.setter
    def before(self, before):
        """Sets the before of this TimeWindowViolation.


        :param before: The before of this TimeWindowViolation.  # noqa: E501
        :type before: ObjectsMetrics
        """

        self._before = before

    @property
    def after(self):
        """Gets the after of this TimeWindowViolation.  # noqa: E501


        :return: The after of this TimeWindowViolation.  # noqa: E501
        :rtype: ObjectsMetrics
        """
        return self._after

    @after.setter
    def after(self, after):
        """Sets the after of this TimeWindowViolation.


        :param after: The after of this TimeWindowViolation.  # noqa: E501
        :type after: ObjectsMetrics
        """

        self._after = after

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
        if not isinstance(other, TimeWindowViolation):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TimeWindowViolation):
            return True

        return self.to_dict() != other.to_dict()
