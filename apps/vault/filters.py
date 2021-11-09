from common.drf.filters import BaseFilterSet

from vault.models import Account


class AccountFilter(BaseFilterSet):
    class Meta:
        model = Account
        fields = (
            'id', 'name', 'username', 'protocol', 'is_privileged'
        )
