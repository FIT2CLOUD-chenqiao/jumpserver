# coding: utf-8
#
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

from common.utils import get_logger
from common.utils.ip import is_ip_address, is_ip_network, is_ip_segment

logger = get_logger(__file__)

__all__ = ['RuleSerializer']


def ip_group_child_validator(ip_group_child):
    is_valid = ip_group_child == '*' \
               or is_ip_address(ip_group_child) \
               or is_ip_network(ip_group_child) \
               or is_ip_segment(ip_group_child)
    if not is_valid:
        error = _('IP address invalid: `{}`').format(ip_group_child)
        raise serializers.ValidationError(error)


class RuleSerializer(serializers.Serializer):
    ip_group_help_text = _(
        'Format for comma-delimited string, with * indicating a match all. '
        'Such as: '
        '192.168.10.1, 192.168.1.0/24, 10.1.1.1-10.1.1.20, 2001:db8:2de::e13, 2001:db8:1a:1110::/64 '
    )

    ip_group = serializers.ListField(
        default=['*'], label=_('IP'), help_text=ip_group_help_text,
        child=serializers.CharField(max_length=1024, validators=[ip_group_child_validator]))
    time_period = serializers.ListField(default=[], label=_('Time Period'))
