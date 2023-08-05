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


class Order(object):
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
        'key': 'str',
        'order_features': 'list[str]',
        'order_restrictions': 'list[str]',
        'performer_restrictions': 'list[str]',
        'performer_blacklist': 'list[str]',
        'cargos': 'list[Cargo]',
        'demands': 'list[Demand]',
        'attributes': 'list[str]'
    }

    attribute_map = {
        'key': 'key',
        'order_features': 'order_features',
        'order_restrictions': 'order_restrictions',
        'performer_restrictions': 'performer_restrictions',
        'performer_blacklist': 'performer_blacklist',
        'cargos': 'cargos',
        'demands': 'demands',
        'attributes': 'attributes'
    }

    def __init__(self, key=None, order_features=None, order_restrictions=None, performer_restrictions=[], performer_blacklist=[], cargos=None, demands=None, attributes=[], local_vars_configuration=None):  # noqa: E501
        """Order - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._key = None
        self._order_features = None
        self._order_restrictions = None
        self._performer_restrictions = None
        self._performer_blacklist = None
        self._cargos = None
        self._demands = None
        self._attributes = None
        self.discriminator = None

        self.key = key
        if order_features is not None:
            self.order_features = order_features
        if order_restrictions is not None:
            self.order_restrictions = order_restrictions
        if performer_restrictions is not None:
            self.performer_restrictions = performer_restrictions
        if performer_blacklist is not None:
            self.performer_blacklist = performer_blacklist
        if cargos is not None:
            self.cargos = cargos
        self.demands = demands
        if attributes is not None:
            self.attributes = attributes

    @property
    def key(self):
        """Gets the key of this Order.  # noqa: E501

        Order key, unique ID.  # noqa: E501

        :return: The key of this Order.  # noqa: E501
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """Sets the key of this Order.

        Order key, unique ID.  # noqa: E501

        :param key: The key of this Order.  # noqa: E501
        :type key: str
        """
        if self.local_vars_configuration.client_side_validation and key is None:  # noqa: E501
            raise ValueError("Invalid value for `key`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                key is not None and len(key) > 1024):
            raise ValueError("Invalid value for `key`, length must be less than or equal to `1024`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                key is not None and len(key) < 1):
            raise ValueError("Invalid value for `key`, length must be greater than or equal to `1`")  # noqa: E501

        self._key = key

    @property
    def order_features(self):
        """Gets the order_features of this Order.  # noqa: E501

        Order features list.  # noqa: E501

        :return: The order_features of this Order.  # noqa: E501
        :rtype: list[str]
        """
        return self._order_features

    @order_features.setter
    def order_features(self, order_features):
        """Sets the order_features of this Order.

        Order features list.  # noqa: E501

        :param order_features: The order_features of this Order.  # noqa: E501
        :type order_features: list[str]
        """
        if (self.local_vars_configuration.client_side_validation and
                order_features is not None and len(order_features) > 1000):
            raise ValueError("Invalid value for `order_features`, number of items must be less than or equal to `1000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                order_features is not None and len(order_features) < 0):
            raise ValueError("Invalid value for `order_features`, number of items must be greater than or equal to `0`")  # noqa: E501

        self._order_features = order_features

    @property
    def order_restrictions(self):
        """Gets the order_restrictions of this Order.  # noqa: E501

        List of requirements for an order being delivered during the same trip.  # noqa: E501

        :return: The order_restrictions of this Order.  # noqa: E501
        :rtype: list[str]
        """
        return self._order_restrictions

    @order_restrictions.setter
    def order_restrictions(self, order_restrictions):
        """Sets the order_restrictions of this Order.

        List of requirements for an order being delivered during the same trip.  # noqa: E501

        :param order_restrictions: The order_restrictions of this Order.  # noqa: E501
        :type order_restrictions: list[str]
        """
        if (self.local_vars_configuration.client_side_validation and
                order_restrictions is not None and len(order_restrictions) > 1000):
            raise ValueError("Invalid value for `order_restrictions`, number of items must be less than or equal to `1000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                order_restrictions is not None and len(order_restrictions) < 0):
            raise ValueError("Invalid value for `order_restrictions`, number of items must be greater than or equal to `0`")  # noqa: E501

        self._order_restrictions = order_restrictions

    @property
    def performer_restrictions(self):
        """Gets the performer_restrictions of this Order.  # noqa: E501

        Requirements list for the performer. Used for checking the compatibility of the performer and the order (work).   # noqa: E501

        :return: The performer_restrictions of this Order.  # noqa: E501
        :rtype: list[str]
        """
        return self._performer_restrictions

    @performer_restrictions.setter
    def performer_restrictions(self, performer_restrictions):
        """Sets the performer_restrictions of this Order.

        Requirements list for the performer. Used for checking the compatibility of the performer and the order (work).   # noqa: E501

        :param performer_restrictions: The performer_restrictions of this Order.  # noqa: E501
        :type performer_restrictions: list[str]
        """
        if (self.local_vars_configuration.client_side_validation and
                performer_restrictions is not None and len(performer_restrictions) > 1000):
            raise ValueError("Invalid value for `performer_restrictions`, number of items must be less than or equal to `1000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                performer_restrictions is not None and len(performer_restrictions) < 0):
            raise ValueError("Invalid value for `performer_restrictions`, number of items must be greater than or equal to `0`")  # noqa: E501

        self._performer_restrictions = performer_restrictions

    @property
    def performer_blacklist(self):
        """Gets the performer_blacklist of this Order.  # noqa: E501

        A list of requirements that the performer is not allowed to have. Used for checking the compatibility of the performer and the order (work). This list should not intersect with `performer_restrictions`.   # noqa: E501

        :return: The performer_blacklist of this Order.  # noqa: E501
        :rtype: list[str]
        """
        return self._performer_blacklist

    @performer_blacklist.setter
    def performer_blacklist(self, performer_blacklist):
        """Sets the performer_blacklist of this Order.

        A list of requirements that the performer is not allowed to have. Used for checking the compatibility of the performer and the order (work). This list should not intersect with `performer_restrictions`.   # noqa: E501

        :param performer_blacklist: The performer_blacklist of this Order.  # noqa: E501
        :type performer_blacklist: list[str]
        """
        if (self.local_vars_configuration.client_side_validation and
                performer_blacklist is not None and len(performer_blacklist) > 1000):
            raise ValueError("Invalid value for `performer_blacklist`, number of items must be less than or equal to `1000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                performer_blacklist is not None and len(performer_blacklist) < 0):
            raise ValueError("Invalid value for `performer_blacklist`, number of items must be greater than or equal to `0`")  # noqa: E501

        self._performer_blacklist = performer_blacklist

    @property
    def cargos(self):
        """Gets the cargos of this Order.  # noqa: E501

        Cargo list (can contain one cargo for `DROP`, a list for `PICKUP`, should be empty for `WORK`).  # noqa: E501

        :return: The cargos of this Order.  # noqa: E501
        :rtype: list[Cargo]
        """
        return self._cargos

    @cargos.setter
    def cargos(self, cargos):
        """Sets the cargos of this Order.

        Cargo list (can contain one cargo for `DROP`, a list for `PICKUP`, should be empty for `WORK`).  # noqa: E501

        :param cargos: The cargos of this Order.  # noqa: E501
        :type cargos: list[Cargo]
        """
        if (self.local_vars_configuration.client_side_validation and
                cargos is not None and len(cargos) > 1000):
            raise ValueError("Invalid value for `cargos`, number of items must be less than or equal to `1000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                cargos is not None and len(cargos) < 0):
            raise ValueError("Invalid value for `cargos`, number of items must be greater than or equal to `0`")  # noqa: E501

        self._cargos = cargos

    @property
    def demands(self):
        """Gets the demands of this Order.  # noqa: E501

        Demands list.  # noqa: E501

        :return: The demands of this Order.  # noqa: E501
        :rtype: list[Demand]
        """
        return self._demands

    @demands.setter
    def demands(self, demands):
        """Sets the demands of this Order.

        Demands list.  # noqa: E501

        :param demands: The demands of this Order.  # noqa: E501
        :type demands: list[Demand]
        """
        if self.local_vars_configuration.client_side_validation and demands is None:  # noqa: E501
            raise ValueError("Invalid value for `demands`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                demands is not None and len(demands) > 1000):
            raise ValueError("Invalid value for `demands`, number of items must be less than or equal to `1000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                demands is not None and len(demands) < 1):
            raise ValueError("Invalid value for `demands`, number of items must be greater than or equal to `1`")  # noqa: E501

        self._demands = demands

    @property
    def attributes(self):
        """Gets the attributes of this Order.  # noqa: E501

        Attributes, used to add service information that does not affect planning.  # noqa: E501

        :return: The attributes of this Order.  # noqa: E501
        :rtype: list[str]
        """
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        """Sets the attributes of this Order.

        Attributes, used to add service information that does not affect planning.  # noqa: E501

        :param attributes: The attributes of this Order.  # noqa: E501
        :type attributes: list[str]
        """
        if (self.local_vars_configuration.client_side_validation and
                attributes is not None and len(attributes) > 1000):
            raise ValueError("Invalid value for `attributes`, number of items must be less than or equal to `1000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                attributes is not None and len(attributes) < 0):
            raise ValueError("Invalid value for `attributes`, number of items must be greater than or equal to `0`")  # noqa: E501

        self._attributes = attributes

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
        if not isinstance(other, Order):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Order):
            return True

        return self.to_dict() != other.to_dict()
