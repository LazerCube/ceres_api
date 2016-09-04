from rest_framework import serializers
from relationships.models import Relationship, Friend

class RelationshipSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Relationship
        fields = (
            'url', 'target_user', 'blocking', 'muting',
            'marked_as_spam', 'notifications_enabled',
            'created_at', 'updated_at'
        )
        read_only_fields = ('url', 'target_user', 'created_at', 'updated_at')

class FriendSerializer(serializers.HyperlinkedModelSerializer):

    friend_name = serializers.ReadOnlyField(source='target_user.username')

    class Meta:
        model =  Friend
        fields = ('friend_name', 'url', 'source_user', 'target_user', 'confirmed', 'created_at', 'updated_at')
        read_only_fields = ('url', 'source_user', 'target_user', 'confirmed', 'created_at', 'updated_at')
