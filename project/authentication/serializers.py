from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from authentication.models import Account


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    relationships = serializers.HyperlinkedIdentityField(view_name='account-relationships-list', lookup_url_kwarg='account_pk')
    friends = serializers.HyperlinkedIdentityField(view_name='account-friends-list', lookup_url_kwarg='account_pk')
    activity = serializers.HyperlinkedIdentityField(view_name='account-activity-list', lookup_url_kwarg='account_pk')

    class Meta:
        model = Account
        fields = ('url', 'relationships', 'friends', 'activity', 'id', 'slug', 'email', 'username',
                  'first_name', 'last_name', 'password',
                  'confirm_password', 'created_at', 'updated_at')
        read_only_fields = ('url','id','slug', 'friends', 'created_at', 'updated_at')

        def create(self, validated_data):
            return Account.objects.create(**validated_data)

        def update(self, instance, validated_data):
            instance.username = validated_data.get('username', instance.username)
            instance.email = validated_data.get('email', instance.email)
            instance.first_name = validated_data.get('first_name', instance.first_name)
            instance.last_name = validated_data.get('last_name', instance.last_name)

            instance.save()

            password = validated_data.get('password', None)
            confirm_password = validated_data.get('confirm_password', None)

            if password and confirm_password and password == confirm_password:
                instance.set_password(password)
                instance.save()

            update_session_auth_hash(self.context.get('request'), instance)

            return instance
