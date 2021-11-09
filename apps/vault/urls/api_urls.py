from django.urls import path
from rest_framework_bulk.routes import BulkRouter

from .. import api

app_name = 'vaults'
router = BulkRouter()
router.register('tickets', api.AccountViewSet, 'ticket')

urlpatterns = [
    path('testing', api.VaultConnectTestingAPI.as_view(), name='vault-connect-testing')
]

urlpatterns += router.urls
