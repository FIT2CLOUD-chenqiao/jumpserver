# -*- coding: utf-8 -*-
#
from django.utils.translation import ugettext_lazy as _
from orgs.mixins.serializers import OrgResourceModelSerializerMixin
from vault.models import Account

__all__ = [
    'AccountSerializer',
]


class AccountSerializer(OrgResourceModelSerializerMixin):
    class Meta:
        model = Account
        fields_mini = ['id', 'name']
        fields_small = fields_mini + [
            'protocol', 'is_privileged', 'org_id', 'org_name', 'comment'
        ]
        fields = fields_small
