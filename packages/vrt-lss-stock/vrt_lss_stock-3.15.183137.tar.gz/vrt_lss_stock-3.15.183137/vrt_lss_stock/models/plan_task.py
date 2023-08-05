# coding: utf-8

"""
    Veeroute.Stock

    Veeroute Stock API  # noqa: E501

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

from vrt_lss_stock.configuration import Configuration


class PlanTask(object):
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
        'storages': 'list[Storage]'
    }

    attribute_map = {
        'storages': 'storages'
    }

    def __init__(self, storages=None, local_vars_configuration=None):  # noqa: E501
        """PlanTask - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._storages = None
        self.discriminator = None

        self.storages = storages

    @property
    def storages(self):
        """Gets the storages of this PlanTask.  # noqa: E501

        List of storages.  # noqa: E501

        :return: The storages of this PlanTask.  # noqa: E501
        :rtype: list[Storage]
        """
        return self._storages

    @storages.setter
    def storages(self, storages):
        """Sets the storages of this PlanTask.

        List of storages.  # noqa: E501

        :param storages: The storages of this PlanTask.  # noqa: E501
        :type storages: list[Storage]
        """
        if self.local_vars_configuration.client_side_validation and storages is None:  # noqa: E501
            raise ValueError("Invalid value for `storages`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                storages is not None and len(storages) > 10000):
            raise ValueError("Invalid value for `storages`, number of items must be less than or equal to `10000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                storages is not None and len(storages) < 1):
            raise ValueError("Invalid value for `storages`, number of items must be greater than or equal to `1`")  # noqa: E501

        self._storages = storages

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
        if not isinstance(other, PlanTask):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PlanTask):
            return True

        return self.to_dict() != other.to_dict()
