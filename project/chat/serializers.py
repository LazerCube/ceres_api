from rest_framework.fields import CurrentUserDefault

from rest_framework import serializers
from chat.models import Room, Message

from rest_framework.reverse import reverse

from rest_framework import serializers
from rest_framework.reverse import reverse

class MessageSerializer(serializers.HyperlinkedModelSerializer):
    '''Serializar for the Message model which is part of the room model'''
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Message
        lookup_field = 'pk2'
        fields = ('id', 'url', 'room', 'msg_type', 'author', 'message', 'created_at', 'updated_at')
        read_only_fields =('id', 'url', 'created_at', 'updated_at')

    def create(self, validated_data):
        room = validated_data.get('room', '')
        msg_type = validated_data.get('msg_type', '')
        message = validated_data.get('message', '')
        author = validated_data.get('auth_user')

        instance = Room.objects.get(pk=room.pk)
        return instance.create_message(msg_type, author, message)

class RoomSerializer(serializers.HyperlinkedModelSerializer):
    '''Serializar for the Room model'''

    history = serializers.HyperlinkedIdentityField(view_name='room-history')

    class Meta:
        model = Room
        lookup_field = 'pk'
        fields = ('id', 'url', 'name', 'description','created_at', 'updated_at', 'history')
        read_only_fields = ('id', 'url', 'created_at', 'updated_at')

    def create(self, validated_data):
        user = validated_data.get('auth_user')
        name = validated_data.get('name', '')
        desc = validated_data.get('description', '')

        return Room.objects.get_or_create(user, name, desc)
