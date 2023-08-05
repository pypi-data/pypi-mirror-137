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


class PlanAssumptions(object):
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
        'traffic_jams': 'bool',
        'toll_roads': 'bool',
        'ferry_crossing': 'bool',
        'flight_distance': 'bool',
        'disable_compatibility': 'bool',
        'disable_capacity': 'bool',
        'same_order_time_window': 'bool',
        'expand_shift_time_window': 'bool'
    }

    attribute_map = {
        'traffic_jams': 'traffic_jams',
        'toll_roads': 'toll_roads',
        'ferry_crossing': 'ferry_crossing',
        'flight_distance': 'flight_distance',
        'disable_compatibility': 'disable_compatibility',
        'disable_capacity': 'disable_capacity',
        'same_order_time_window': 'same_order_time_window',
        'expand_shift_time_window': 'expand_shift_time_window'
    }

    def __init__(self, traffic_jams=True, toll_roads=True, ferry_crossing=True, flight_distance=False, disable_compatibility=False, disable_capacity=False, same_order_time_window=False, expand_shift_time_window=False, local_vars_configuration=None):  # noqa: E501
        """PlanAssumptions - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._traffic_jams = None
        self._toll_roads = None
        self._ferry_crossing = None
        self._flight_distance = None
        self._disable_compatibility = None
        self._disable_capacity = None
        self._same_order_time_window = None
        self._expand_shift_time_window = None
        self.discriminator = None

        if traffic_jams is not None:
            self.traffic_jams = traffic_jams
        if toll_roads is not None:
            self.toll_roads = toll_roads
        if ferry_crossing is not None:
            self.ferry_crossing = ferry_crossing
        if flight_distance is not None:
            self.flight_distance = flight_distance
        if disable_compatibility is not None:
            self.disable_compatibility = disable_compatibility
        if disable_capacity is not None:
            self.disable_capacity = disable_capacity
        if same_order_time_window is not None:
            self.same_order_time_window = same_order_time_window
        if expand_shift_time_window is not None:
            self.expand_shift_time_window = expand_shift_time_window

    @property
    def traffic_jams(self):
        """Gets the traffic_jams of this PlanAssumptions.  # noqa: E501

        Accounting for traffic during the route planning.  # noqa: E501

        :return: The traffic_jams of this PlanAssumptions.  # noqa: E501
        :rtype: bool
        """
        return self._traffic_jams

    @traffic_jams.setter
    def traffic_jams(self, traffic_jams):
        """Sets the traffic_jams of this PlanAssumptions.

        Accounting for traffic during the route planning.  # noqa: E501

        :param traffic_jams: The traffic_jams of this PlanAssumptions.  # noqa: E501
        :type traffic_jams: bool
        """

        self._traffic_jams = traffic_jams

    @property
    def toll_roads(self):
        """Gets the toll_roads of this PlanAssumptions.  # noqa: E501

        Use toll roads.  # noqa: E501

        :return: The toll_roads of this PlanAssumptions.  # noqa: E501
        :rtype: bool
        """
        return self._toll_roads

    @toll_roads.setter
    def toll_roads(self, toll_roads):
        """Sets the toll_roads of this PlanAssumptions.

        Use toll roads.  # noqa: E501

        :param toll_roads: The toll_roads of this PlanAssumptions.  # noqa: E501
        :type toll_roads: bool
        """

        self._toll_roads = toll_roads

    @property
    def ferry_crossing(self):
        """Gets the ferry_crossing of this PlanAssumptions.  # noqa: E501

        Use ferry crossing.  # noqa: E501

        :return: The ferry_crossing of this PlanAssumptions.  # noqa: E501
        :rtype: bool
        """
        return self._ferry_crossing

    @ferry_crossing.setter
    def ferry_crossing(self, ferry_crossing):
        """Sets the ferry_crossing of this PlanAssumptions.

        Use ferry crossing.  # noqa: E501

        :param ferry_crossing: The ferry_crossing of this PlanAssumptions.  # noqa: E501
        :type ferry_crossing: bool
        """

        self._ferry_crossing = ferry_crossing

    @property
    def flight_distance(self):
        """Gets the flight_distance of this PlanAssumptions.  # noqa: E501

        Use for calculating straight line distances. If `false` is specified, distances are calculated by roads. When this parameter is enabled, traffic tracking (`traffic_jams`) is automatically disabled.   # noqa: E501

        :return: The flight_distance of this PlanAssumptions.  # noqa: E501
        :rtype: bool
        """
        return self._flight_distance

    @flight_distance.setter
    def flight_distance(self, flight_distance):
        """Sets the flight_distance of this PlanAssumptions.

        Use for calculating straight line distances. If `false` is specified, distances are calculated by roads. When this parameter is enabled, traffic tracking (`traffic_jams`) is automatically disabled.   # noqa: E501

        :param flight_distance: The flight_distance of this PlanAssumptions.  # noqa: E501
        :type flight_distance: bool
        """

        self._flight_distance = flight_distance

    @property
    def disable_compatibility(self):
        """Gets the disable_compatibility of this PlanAssumptions.  # noqa: E501

        Disable the accounting for capacity. If `true` is specified, all becomes compatible with everything.   # noqa: E501

        :return: The disable_compatibility of this PlanAssumptions.  # noqa: E501
        :rtype: bool
        """
        return self._disable_compatibility

    @disable_compatibility.setter
    def disable_compatibility(self, disable_compatibility):
        """Sets the disable_compatibility of this PlanAssumptions.

        Disable the accounting for capacity. If `true` is specified, all becomes compatible with everything.   # noqa: E501

        :param disable_compatibility: The disable_compatibility of this PlanAssumptions.  # noqa: E501
        :type disable_compatibility: bool
        """

        self._disable_compatibility = disable_compatibility

    @property
    def disable_capacity(self):
        """Gets the disable_capacity of this PlanAssumptions.  # noqa: E501

        Disable the accounting for capacity. If `true` is specified, all vehicles can accommodate an unlimited cargo amount.   # noqa: E501

        :return: The disable_capacity of this PlanAssumptions.  # noqa: E501
        :rtype: bool
        """
        return self._disable_capacity

    @disable_capacity.setter
    def disable_capacity(self, disable_capacity):
        """Sets the disable_capacity of this PlanAssumptions.

        Disable the accounting for capacity. If `true` is specified, all vehicles can accommodate an unlimited cargo amount.   # noqa: E501

        :param disable_capacity: The disable_capacity of this PlanAssumptions.  # noqa: E501
        :type disable_capacity: bool
        """

        self._disable_capacity = disable_capacity

    @property
    def same_order_time_window(self):
        """Gets the same_order_time_window of this PlanAssumptions.  # noqa: E501

        Use for calculation the same (specified) time window for orders and demands. The time window is specified from the beginning of the earliest window to the end of the latest window from all orders and demands.   # noqa: E501

        :return: The same_order_time_window of this PlanAssumptions.  # noqa: E501
        :rtype: bool
        """
        return self._same_order_time_window

    @same_order_time_window.setter
    def same_order_time_window(self, same_order_time_window):
        """Sets the same_order_time_window of this PlanAssumptions.

        Use for calculation the same (specified) time window for orders and demands. The time window is specified from the beginning of the earliest window to the end of the latest window from all orders and demands.   # noqa: E501

        :param same_order_time_window: The same_order_time_window of this PlanAssumptions.  # noqa: E501
        :type same_order_time_window: bool
        """

        self._same_order_time_window = same_order_time_window

    @property
    def expand_shift_time_window(self):
        """Gets the expand_shift_time_window of this PlanAssumptions.  # noqa: E501

        Expand the time window for performers' and vehicle shifts.  The left border of the first shift extends to the left border of the specified window, right border extends to the right border or to the beginning of the next window for this entity. Each next shift moves the right border to the next shift or to the right border of the specified window.   # noqa: E501

        :return: The expand_shift_time_window of this PlanAssumptions.  # noqa: E501
        :rtype: bool
        """
        return self._expand_shift_time_window

    @expand_shift_time_window.setter
    def expand_shift_time_window(self, expand_shift_time_window):
        """Sets the expand_shift_time_window of this PlanAssumptions.

        Expand the time window for performers' and vehicle shifts.  The left border of the first shift extends to the left border of the specified window, right border extends to the right border or to the beginning of the next window for this entity. Each next shift moves the right border to the next shift or to the right border of the specified window.   # noqa: E501

        :param expand_shift_time_window: The expand_shift_time_window of this PlanAssumptions.  # noqa: E501
        :type expand_shift_time_window: bool
        """

        self._expand_shift_time_window = expand_shift_time_window

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
        if not isinstance(other, PlanAssumptions):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PlanAssumptions):
            return True

        return self.to_dict() != other.to_dict()
