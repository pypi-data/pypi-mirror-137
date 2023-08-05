# coding: utf-8

"""
    AssistedInstall

    Assisted installation  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class ServiceNetwork(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'cluster_id': 'str',
        'cidr': 'Subnet'
    }

    attribute_map = {
        'cluster_id': 'cluster_id',
        'cidr': 'cidr'
    }

    def __init__(self, cluster_id=None, cidr=None):  # noqa: E501
        """ServiceNetwork - a model defined in Swagger"""  # noqa: E501

        self._cluster_id = None
        self._cidr = None
        self.discriminator = None

        if cluster_id is not None:
            self.cluster_id = cluster_id
        if cidr is not None:
            self.cidr = cidr

    @property
    def cluster_id(self):
        """Gets the cluster_id of this ServiceNetwork.  # noqa: E501

        The cluster that this network is associated with.  # noqa: E501

        :return: The cluster_id of this ServiceNetwork.  # noqa: E501
        :rtype: str
        """
        return self._cluster_id

    @cluster_id.setter
    def cluster_id(self, cluster_id):
        """Sets the cluster_id of this ServiceNetwork.

        The cluster that this network is associated with.  # noqa: E501

        :param cluster_id: The cluster_id of this ServiceNetwork.  # noqa: E501
        :type: str
        """

        self._cluster_id = cluster_id

    @property
    def cidr(self):
        """Gets the cidr of this ServiceNetwork.  # noqa: E501

        The IP block address pool.  # noqa: E501

        :return: The cidr of this ServiceNetwork.  # noqa: E501
        :rtype: Subnet
        """
        return self._cidr

    @cidr.setter
    def cidr(self, cidr):
        """Sets the cidr of this ServiceNetwork.

        The IP block address pool.  # noqa: E501

        :param cidr: The cidr of this ServiceNetwork.  # noqa: E501
        :type: Subnet
        """

        self._cidr = cidr

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(ServiceNetwork, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ServiceNetwork):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
