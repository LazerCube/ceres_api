from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import detail_route, list_route

from rest_framework.generics import get_object_or_404
from rest_framework.mixins import (
    RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin, CreateModelMixin
)

from django.db.models import Q

from rest_framework.permissions import DjangoModelPermissions
from authentication.permissions import IsAuthenticatedOrTokenHasReadWriteScope, IsOwnerOrReadOnly
from relationships.permissions import IsSource, IsSourceUserOrPost

from authentication.models import Account

from relationships.models import Relationship, Friend
from relationships.serializers import RelationshipSerializer
from relationships.serializers import FriendSerializer

class RelationshipViewSet(ModelViewSet):
    serializer_class = RelationshipSerializer
    queryset = Relationship.objects.all()
    permission_classes = [IsAuthenticatedOrTokenHasReadWriteScope, IsSourceUserOrPost]

    def get_queryset(self):
        user = self.request.user
        return Relationship.objects.filter(source_user=user)

    def perform_create(self, serializer):
        serializer.save(source_user=self.request.user)

class FriendViewSet(
    RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet
):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer
    permission_classes = [IsAuthenticatedOrTokenHasReadWriteScope, IsSource]

    def get_queryset(self):
        user = self.request.user
        return Friend.objects.filter(source_user=user)

    def perform_destroy(self, instance):
        Friend.objects.delete_remove_friend(instance)

class NestedFriendViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer
    permission_classes = [IsAuthenticatedOrTokenHasReadWriteScope]

    def get_account(self, request, account_pk=None):
        account = get_object_or_404(Account.objects.all(), pk=account_pk)
        self.check_object_permissions(self.request, account)
        return account

    def create(self, request, *args, **kwargs):
        account = self.get_account(request, account_pk=kwargs['account_pk'])
        friend = Friend.objects.create_or_make_friends(source_user=self.request.user, target_user=account)
        serializer = self.get_serializer(friend, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        return Friend.objects.filter(source_user=self.kwargs['account_pk'], confirmed=True)

    def list(self, request, *args, **kwargs):
        self.get_account(request, account_pk=kwargs['account_pk'])
        return super(NestedFriendViewSet, self).list(request, *args, **kwargs)

    # permission_classes=[IsSource]
    @list_route(methods=['get'], url_path='outgoing')
    def get_outgoing(self, request, *args, **kwargs):
        self.get_account(request, account_pk=kwargs['account_pk'])
        queryset = Friend.objects.filter(source_user=self.kwargs['account_pk'], confirmed=False)
        return self.gen_paginate(queryset)

    @list_route(methods=['get'], url_path='incoming')
    def get_incoming(self, request, *args, **kwargs):
        self.get_account(request, account_pk=kwargs['account_pk'])
        queryset = Friend.objects.filter(target_user=self.kwargs['account_pk'], confirmed=False)
        return self.gen_paginate(queryset)

    def gen_paginate(self, queryset):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(recent_users, many=True)
        return Response(serializer.data)
