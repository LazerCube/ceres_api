from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.generics import get_object_or_404

from authentication.permissions import IsAuthenticatedOrTokenHasReadWriteScope
from authentication.models import Account

from activity.serializers import ActivitySerializer
from activity.models import Activity

class ActivityViewSet(ReadOnlyModelViewSet):
    serializer_class = ActivitySerializer
    queryset = Activity.objects.all()
    permission_classes = [IsAuthenticatedOrTokenHasReadWriteScope]

class NestedActivityViewSet(ReadOnlyModelViewSet):
    serializer_class = ActivitySerializer
    queryset = Activity.objects.all()
    permission_classes = [IsAuthenticatedOrTokenHasReadWriteScope]

    def get_account(self, request, account_pk=None):
        account = get_object_or_404(Account.objects.all(), pk=account_pk)
        self.check_object_permissions(request, account)
        return account

    def get_queryset(self):
        account = self.get_account(self.request, account_pk=self.kwargs['account_pk'])
        return Activity.objects.user(account, with_user_activity=True).order_by('-timestamp')

    def list(self, request, *args, **kwargs):
        self.get_account(request, account_pk=kwargs['account_pk'])
        return super(NestedActivityViewSet, self).list(request, *args, **kwargs)
