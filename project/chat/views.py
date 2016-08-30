from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from rest_framework.generics import get_object_or_404
from rest_framework.mixins import (
    RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin, CreateModelMixin
)

from core.pagination import StandardResultsSetPagination

from rest_framework.permissions import DjangoModelPermissions
from authentication.permissions import IsAuthenticatedOrTokenHasReadWriteScope, IsOwnerOrReadOnly

from chat.models import Room, Message
from chat.serializers import RoomSerializer, MessageSerializer

class RoomViewSet(ModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    permission_classes = [IsAuthenticatedOrTokenHasReadWriteScope, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MessageViewSet(
    RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet
):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticatedOrTokenHasReadWriteScope, IsOwnerOrReadOnly]

class NestedMessageViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticatedOrTokenHasReadWriteScope]

    def get_room(self, request, room_pk=None):
        room = get_object_or_404(Room.objects.all(), pk=room_pk)
        self.check_object_permissions(self.request, room)
        return room

    def create(self, request, *args, **kwargs):
        self.get_room(request, room_pk=kwargs['room_pk'])
        return super(NestedMessageViewSet, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            id=self.kwargs['room_pk']
        )

    def get_queryset(self):
        return Message.objects.filter(room=self.kwargs['room_pk'])

    def list(self, request, *args, **kwargs):
        self.get_room(request, room_pk=kwargs['room_pk'])
        return super(NestedMessageViewSet, self).list(request, *args, **kwargs)
