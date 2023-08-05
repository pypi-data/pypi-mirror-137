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


class ClusterProgressInfo(object):
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
        'total_percentage': 'int',
        'preparing_for_installation_stage_percentage': 'int',
        'installing_stage_percentage': 'int',
        'finalizing_stage_percentage': 'int'
    }

    attribute_map = {
        'total_percentage': 'total_percentage',
        'preparing_for_installation_stage_percentage': 'preparing_for_installation_stage_percentage',
        'installing_stage_percentage': 'installing_stage_percentage',
        'finalizing_stage_percentage': 'finalizing_stage_percentage'
    }

    def __init__(self, total_percentage=None, preparing_for_installation_stage_percentage=None, installing_stage_percentage=None, finalizing_stage_percentage=None):  # noqa: E501
        """ClusterProgressInfo - a model defined in Swagger"""  # noqa: E501

        self._total_percentage = None
        self._preparing_for_installation_stage_percentage = None
        self._installing_stage_percentage = None
        self._finalizing_stage_percentage = None
        self.discriminator = None

        if total_percentage is not None:
            self.total_percentage = total_percentage
        if preparing_for_installation_stage_percentage is not None:
            self.preparing_for_installation_stage_percentage = preparing_for_installation_stage_percentage
        if installing_stage_percentage is not None:
            self.installing_stage_percentage = installing_stage_percentage
        if finalizing_stage_percentage is not None:
            self.finalizing_stage_percentage = finalizing_stage_percentage

    @property
    def total_percentage(self):
        """Gets the total_percentage of this ClusterProgressInfo.  # noqa: E501


        :return: The total_percentage of this ClusterProgressInfo.  # noqa: E501
        :rtype: int
        """
        return self._total_percentage

    @total_percentage.setter
    def total_percentage(self, total_percentage):
        """Sets the total_percentage of this ClusterProgressInfo.


        :param total_percentage: The total_percentage of this ClusterProgressInfo.  # noqa: E501
        :type: int
        """

        self._total_percentage = total_percentage

    @property
    def preparing_for_installation_stage_percentage(self):
        """Gets the preparing_for_installation_stage_percentage of this ClusterProgressInfo.  # noqa: E501


        :return: The preparing_for_installation_stage_percentage of this ClusterProgressInfo.  # noqa: E501
        :rtype: int
        """
        return self._preparing_for_installation_stage_percentage

    @preparing_for_installation_stage_percentage.setter
    def preparing_for_installation_stage_percentage(self, preparing_for_installation_stage_percentage):
        """Sets the preparing_for_installation_stage_percentage of this ClusterProgressInfo.


        :param preparing_for_installation_stage_percentage: The preparing_for_installation_stage_percentage of this ClusterProgressInfo.  # noqa: E501
        :type: int
        """

        self._preparing_for_installation_stage_percentage = preparing_for_installation_stage_percentage

    @property
    def installing_stage_percentage(self):
        """Gets the installing_stage_percentage of this ClusterProgressInfo.  # noqa: E501


        :return: The installing_stage_percentage of this ClusterProgressInfo.  # noqa: E501
        :rtype: int
        """
        return self._installing_stage_percentage

    @installing_stage_percentage.setter
    def installing_stage_percentage(self, installing_stage_percentage):
        """Sets the installing_stage_percentage of this ClusterProgressInfo.


        :param installing_stage_percentage: The installing_stage_percentage of this ClusterProgressInfo.  # noqa: E501
        :type: int
        """

        self._installing_stage_percentage = installing_stage_percentage

    @property
    def finalizing_stage_percentage(self):
        """Gets the finalizing_stage_percentage of this ClusterProgressInfo.  # noqa: E501


        :return: The finalizing_stage_percentage of this ClusterProgressInfo.  # noqa: E501
        :rtype: int
        """
        return self._finalizing_stage_percentage

    @finalizing_stage_percentage.setter
    def finalizing_stage_percentage(self, finalizing_stage_percentage):
        """Sets the finalizing_stage_percentage of this ClusterProgressInfo.


        :param finalizing_stage_percentage: The finalizing_stage_percentage of this ClusterProgressInfo.  # noqa: E501
        :type: int
        """

        self._finalizing_stage_percentage = finalizing_stage_percentage

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
        if issubclass(ClusterProgressInfo, dict):
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
        if not isinstance(other, ClusterProgressInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
