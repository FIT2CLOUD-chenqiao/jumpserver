from rest_framework.response import Response
from rest_framework.decorators import action

from orgs.mixins.api import OrgBulkModelViewSet
from .. import serializers
from ..models import Account
from ..filters import AccountFilter

__all__ = ['AccountViewSet']


class AccountViewSet(OrgBulkModelViewSet):
    model = Account
    filterset_class = AccountFilter
    search_fields = (
        'id', 'name', 'username', 'is_privileged'
    )
    serializer_classes = {
        'default': serializers.AccountSerializer,
    }

    @action(methods=['get'], detail=True, url_path='secret')
    def view_secret(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(obj)
        return Response(serializer.data)
