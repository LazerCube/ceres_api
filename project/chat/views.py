from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

from core.pagination import StandardResultsSetPagination

from chat.models import Room, Message
from chat.serializers import RoomSerializer, MessageSerializer

from rest_framework.permissions import DjangoModelPermissions
from authentication.permissions import IsAuthenticatedOrTokenHasReadWriteScope, IsOwnerOrReadOnly


class RoomViewSet(viewsets.ModelViewSet):
    """
    Room view set
    """

    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticatedOrTokenHasReadWriteScope, IsOwnerOrReadOnly]

    @detail_route(methods=['get'], url_path='history')
    def messages(self, request, pk=None):
        room = self.get_object()
        messages = Message.objects.filter(room=room)

        self.serializer_class = MessageSerializer

        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_users, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(auth_user=self.request.user)

    # @detail_route(methods=['post','get'], url_path='comment')
    # def comment(self, request, pk=None, **kwargs):
    #     room = self.get_object()
    #
    #     self.queryset = Message.objects.filter(room=room)
    #     self.serializer_class = MessageSerializer
    #
    #     if request.method == 'POST':
    #         data = {
    #             'author': self.request.user,
    #             'message': request.data['message'],
    #             'room': room,
    #         }
    #
    #         serializer = MessageSerializer(data=data)
    #
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         else:
    #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         serializer = MessageSerializer(instance=self.queryset, many=True, context={'request': request})
    #         return Response(serializer.data)

class MessageViewSet(viewsets.ModelViewSet):
    """
    Room view set
    """

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticatedOrTokenHasReadWriteScope, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(auth_user=self.request.user)
