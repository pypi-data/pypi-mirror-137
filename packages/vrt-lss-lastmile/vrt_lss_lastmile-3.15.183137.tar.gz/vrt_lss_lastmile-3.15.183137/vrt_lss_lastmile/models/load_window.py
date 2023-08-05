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


class LoadWindow(object):
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
        'time_window': 'TimeWindow',
        'gates_count': 'int'
    }

    attribute_map = {
        'time_window': 'time_window',
        'gates_count': 'gates_count'
    }

    def __init__(self, time_window=None, gates_count=0, local_vars_configuration=None):  # noqa: E501
        """LoadWindow - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._time_window = None
        self._gates_count = None
        self.discriminator = None

        if time_window is not None:
            self.time_window = time_window
        if gates_count is not None:
            self.gates_count = gates_count

    @property
    def time_window(self):
        """Gets the time_window of this LoadWindow.  # noqa: E501


        :return: The time_window of this LoadWindow.  # noqa: E501
        :rtype: TimeWindow
        """
        return self._time_window

    @time_window.setter
    def time_window(self, time_window):
        """Sets the time_window of this LoadWindow.


        :param time_window: The time_window of this LoadWindow.  # noqa: E501
        :type time_window: TimeWindow
        """

        self._time_window = time_window

    @property
    def gates_count(self):
        """Gets the gates_count of this LoadWindow.  # noqa: E501

        The number of vehicles that can be loaded/unloaded simultaneously within this time window.  If 0, the restriction is ignored.  This parameter strongly affects the planning time and quality of the solution.   # noqa: E501

        :return: The gates_count of this LoadWindow.  # noqa: E501
        :rtype: int
        """
        return self._gates_count

    @gates_count.setter
    def gates_count(self, gates_count):
        """Sets the gates_count of this LoadWindow.

        The number of vehicles that can be loaded/unloaded simultaneously within this time window.  If 0, the restriction is ignored.  This parameter strongly affects the planning time and quality of the solution.   # noqa: E501

        :param gates_count: The gates_count of this LoadWindow.  # noqa: E501
        :type gates_count: int
        """
        if (self.local_vars_configuration.client_side_validation and
                gates_count is not None and gates_count > 9000):  # noqa: E501
            raise ValueError("Invalid value for `gates_count`, must be a value less than or equal to `9000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                gates_count is not None and gates_count < 0):  # noqa: E501
            raise ValueError("Invalid value for `gates_count`, must be a value greater than or equal to `0`")  # noqa: E501

        self._gates_count = gates_count

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
        if not isinstance(other, LoadWindow):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, LoadWindow):
            return True

        return self.to_dict() != other.to_dict()
