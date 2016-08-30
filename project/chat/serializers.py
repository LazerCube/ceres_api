from rest_framework import serializers
from chat.models import Room, Message

class RoomSerializer(serializers.HyperlinkedModelSerializer):

    messages = serializers.HyperlinkedIdentityField(view_name='room-messages-list', lookup_url_kwarg='room_pk')

    class Meta:
        model = Room
        fields = ('url', 'title', 'slug', 'description', 'created_at', 'updated_at', 'messages')
        read_only_fields = ('url', 'slug', 'created_at', 'updated_at')

    def create(self, validated_data):
        user = validated_data.get('user')
        name = validated_data.get('title', '')
        desc = validated_data.get('description', '')
        return Room.objects.get_or_create(user, name, desc)

class MessageSerializer(serializers.HyperlinkedModelSerializer):

    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Message
        fields = ('url','author', 'msg_type', 'message', 'created_at', 'updated_at', 'room')
        read_only_fields =('url', 'created_at', 'updated_at')

    def create(self, validated_data):
        author = validated_data.get('author', '')
        msg_type = validated_data.get('msg_type', '')
        message = validated_data.get('message', '')

        room = validated_data.get('id', '')
        instance = Room.objects.get(pk=room)

        return instance.create_message(msg_type, author, message)
