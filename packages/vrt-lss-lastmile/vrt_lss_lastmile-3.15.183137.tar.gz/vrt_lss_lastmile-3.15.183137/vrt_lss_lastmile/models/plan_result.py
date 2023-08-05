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


class PlanResult(object):
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
        'tracedata': 'TraceData',
        'trips': 'list[Trip]',
        'statistics': 'PlanStatistics',
        'validations': 'list[Validation]',
        'unplanned_orders': 'list[UnplannedOrder]',
        'progress': 'int',
        'info': 'PlanInfo'
    }

    attribute_map = {
        'tracedata': 'tracedata',
        'trips': 'trips',
        'statistics': 'statistics',
        'validations': 'validations',
        'unplanned_orders': 'unplanned_orders',
        'progress': 'progress',
        'info': 'info'
    }

    def __init__(self, tracedata=None, trips=None, statistics=None, validations=None, unplanned_orders=None, progress=None, info=None, local_vars_configuration=None):  # noqa: E501
        """PlanResult - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._tracedata = None
        self._trips = None
        self._statistics = None
        self._validations = None
        self._unplanned_orders = None
        self._progress = None
        self._info = None
        self.discriminator = None

        if tracedata is not None:
            self.tracedata = tracedata
        self.trips = trips
        self.statistics = statistics
        if validations is not None:
            self.validations = validations
        if unplanned_orders is not None:
            self.unplanned_orders = unplanned_orders
        if progress is not None:
            self.progress = progress
        if info is not None:
            self.info = info

    @property
    def tracedata(self):
        """Gets the tracedata of this PlanResult.  # noqa: E501


        :return: The tracedata of this PlanResult.  # noqa: E501
        :rtype: TraceData
        """
        return self._tracedata

    @tracedata.setter
    def tracedata(self, tracedata):
        """Sets the tracedata of this PlanResult.


        :param tracedata: The tracedata of this PlanResult.  # noqa: E501
        :type tracedata: TraceData
        """

        self._tracedata = tracedata

    @property
    def trips(self):
        """Gets the trips of this PlanResult.  # noqa: E501

        Schedule of trips assigned to performers.  # noqa: E501

        :return: The trips of this PlanResult.  # noqa: E501
        :rtype: list[Trip]
        """
        return self._trips

    @trips.setter
    def trips(self, trips):
        """Sets the trips of this PlanResult.

        Schedule of trips assigned to performers.  # noqa: E501

        :param trips: The trips of this PlanResult.  # noqa: E501
        :type trips: list[Trip]
        """
        if self.local_vars_configuration.client_side_validation and trips is None:  # noqa: E501
            raise ValueError("Invalid value for `trips`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                trips is not None and len(trips) > 9000):
            raise ValueError("Invalid value for `trips`, number of items must be less than or equal to `9000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                trips is not None and len(trips) < 0):
            raise ValueError("Invalid value for `trips`, number of items must be greater than or equal to `0`")  # noqa: E501

        self._trips = trips

    @property
    def statistics(self):
        """Gets the statistics of this PlanResult.  # noqa: E501


        :return: The statistics of this PlanResult.  # noqa: E501
        :rtype: PlanStatistics
        """
        return self._statistics

    @statistics.setter
    def statistics(self, statistics):
        """Sets the statistics of this PlanResult.


        :param statistics: The statistics of this PlanResult.  # noqa: E501
        :type statistics: PlanStatistics
        """

        self._statistics = statistics

    @property
    def validations(self):
        """Gets the validations of this PlanResult.  # noqa: E501

        Validations list.  # noqa: E501

        :return: The validations of this PlanResult.  # noqa: E501
        :rtype: list[Validation]
        """
        return self._validations

    @validations.setter
    def validations(self, validations):
        """Sets the validations of this PlanResult.

        Validations list.  # noqa: E501

        :param validations: The validations of this PlanResult.  # noqa: E501
        :type validations: list[Validation]
        """
        if (self.local_vars_configuration.client_side_validation and
                validations is not None and len(validations) > 9000):
            raise ValueError("Invalid value for `validations`, number of items must be less than or equal to `9000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                validations is not None and len(validations) < 0):
            raise ValueError("Invalid value for `validations`, number of items must be greater than or equal to `0`")  # noqa: E501

        self._validations = validations

    @property
    def unplanned_orders(self):
        """Gets the unplanned_orders of this PlanResult.  # noqa: E501

        Unassigned orders list.  # noqa: E501

        :return: The unplanned_orders of this PlanResult.  # noqa: E501
        :rtype: list[UnplannedOrder]
        """
        return self._unplanned_orders

    @unplanned_orders.setter
    def unplanned_orders(self, unplanned_orders):
        """Sets the unplanned_orders of this PlanResult.

        Unassigned orders list.  # noqa: E501

        :param unplanned_orders: The unplanned_orders of this PlanResult.  # noqa: E501
        :type unplanned_orders: list[UnplannedOrder]
        """
        if (self.local_vars_configuration.client_side_validation and
                unplanned_orders is not None and len(unplanned_orders) > 9000):
            raise ValueError("Invalid value for `unplanned_orders`, number of items must be less than or equal to `9000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                unplanned_orders is not None and len(unplanned_orders) < 0):
            raise ValueError("Invalid value for `unplanned_orders`, number of items must be greater than or equal to `0`")  # noqa: E501

        self._unplanned_orders = unplanned_orders

    @property
    def progress(self):
        """Gets the progress of this PlanResult.  # noqa: E501

        Planning progress as a percentage. The progress displays the current number of completed steps.   # noqa: E501

        :return: The progress of this PlanResult.  # noqa: E501
        :rtype: int
        """
        return self._progress

    @progress.setter
    def progress(self, progress):
        """Sets the progress of this PlanResult.

        Planning progress as a percentage. The progress displays the current number of completed steps.   # noqa: E501

        :param progress: The progress of this PlanResult.  # noqa: E501
        :type progress: int
        """
        if (self.local_vars_configuration.client_side_validation and
                progress is not None and progress > 100):  # noqa: E501
            raise ValueError("Invalid value for `progress`, must be a value less than or equal to `100`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                progress is not None and progress < 0):  # noqa: E501
            raise ValueError("Invalid value for `progress`, must be a value greater than or equal to `0`")  # noqa: E501

        self._progress = progress

    @property
    def info(self):
        """Gets the info of this PlanResult.  # noqa: E501


        :return: The info of this PlanResult.  # noqa: E501
        :rtype: PlanInfo
        """
        return self._info

    @info.setter
    def info(self, info):
        """Sets the info of this PlanResult.


        :param info: The info of this PlanResult.  # noqa: E501
        :type info: PlanInfo
        """

        self._info = info

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
        if not isinstance(other, PlanResult):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PlanResult):
            return True

        return self.to_dict() != other.to_dict()
