from rest_framework import serializers
from activity.models import Activity

# All possible serializers for generic related fields
from authentication.serializers import AccountSerializer
from chat.serializers import MessageSerializer, RoomSerializer
from relationships.serializers import RelationshipSerializer, FriendSerializer

#All possible models for generic related fields
from authentication.models import Account
from chat.serializers import Message, Room
from relationships.models import Relationship, Friend

from generic_relations.relations import GenericRelatedField

GenericRelatedHyperlinked = GenericRelatedField({
    Account: serializers.HyperlinkedRelatedField(
        queryset=Account.objects.all(),
        view_name='account-detail',
    ),
    Room: serializers.HyperlinkedRelatedField(
        queryset=Room.objects.all(),
        view_name='room-detail',
    ),
    Message: serializers.HyperlinkedRelatedField(
        queryset=Message.objects.all(),
        view_name='message-detail',
    ),
    Friend: serializers.HyperlinkedRelatedField(
        queryset=Friend.objects.all(),
        view_name='friend-detail',
    ),
})

class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    """
    A `Activity` serializer with a `GenericRelatedField` mapping all possible
    models to their respective serializers.
    """

    actor = GenericRelatedHyperlinked
    text = serializers.ReadOnlyField(source="__unicode__")

    target = GenericRelatedField({
        Account: serializers.HyperlinkedRelatedField(
            queryset=Account.objects.all(),
            view_name='account-detail',
        ),
        Room: serializers.HyperlinkedRelatedField(
            queryset=Room.objects.all(),
            view_name='room-detail',
        ),
        Message: serializers.HyperlinkedRelatedField(
            queryset=Message.objects.all(),
            view_name='message-detail',
        ),
        Friend: serializers.HyperlinkedRelatedField(
            queryset=Friend.objects.all(),
            view_name='friend-detail',
        ),
    })

    action_object = GenericRelatedField({
        Account: serializers.HyperlinkedRelatedField(
            queryset=Account.objects.all(),
            view_name='account-detail',
        ),
        Room: serializers.HyperlinkedRelatedField(
            queryset=Room.objects.all(),
            view_name='room-detail',
        ),
        Message: serializers.HyperlinkedRelatedField(
            queryset=Message.objects.all(),
            view_name='message-detail',
        ),
        Friend: serializers.HyperlinkedRelatedField(
            queryset=Friend.objects.all(),
            view_name='friend-detail',
        ),
    })

    class Meta:
        model = Activity
        # fields = ('url','actor','verb','description','target','action_object','public','timestamp')
        # read_only_fields = ('url','actor','verb','description','target','action_object','public','timestamp')
        fields = ('url','actor', 'verb','action_object','target','text','description','public','timestamp')
        read_only_fields = ('url','actor','verb','description','target','action_object','public','timestamp')
