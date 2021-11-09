from django.db import models
from django.utils.translation import ugettext_lazy as _

from common.mixins.models import CommonModelMixin
from orgs.mixins.models import OrgModelMixin
from assets.models.user import ProtocolMixin


class Account(CommonModelMixin, OrgModelMixin):
    name = models.CharField(max_length=128, verbose_name=_('Name'))
    username = models.CharField(max_length=1024, verbose_name=_('Username'))
    protocol = models.CharField(
        max_length=16, choices=ProtocolMixin.Protocol.choices,
        default='ssh', verbose_name=_('Protocol')
    )
    secret = models.JSONField(default=dict, verbose_name=_('Secret'))
    is_privileged = models.BooleanField(default=False, verbose_name=_('Privileged'))
    comment = models.TextField(blank=True, verbose_name=_("Comment"))

    class Meta:
        ordering = ('-date_updated',)
        verbose_name = _('Vault account')

    def __str__(self):
        return '{0.name}({0.username})'.format(self)
