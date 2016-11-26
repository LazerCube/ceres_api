from __future__ import unicode_literals

from django.db import models
from django.db.models import Q

from django.core.exceptions import ValidationError

from core.mixins import UUIDIdMixin
from authentication.models import Account
from chat.models import Room

class FriendManager(models.Manager):
    def are_friends(self, source_user, target_user):
        print("source_user ", source_user)
        print("target_user ", target_user)
        try:
            qs = Friend.objects.filter(
                Q(source_user=source_user, target_user=target_user, confirmed=True) |
                Q(source_user=target_user, target_user=source_user, confirmed=True)
            ).distinct().all()
            if qs:
                return True
            else:
                return False
        except Friend.DoesNotExist:
            return False

    def get_friends(self):
        return Friend.objects.filter(source_user=self.request.user, confirmed=True)
    
    def create_or_make_friends(self, **kwargs):
        source_user = kwargs.get('source_user')
        target_user = kwargs.get('target_user')
        if self.is_pending(source_user, target_user):
            friend = Friend.objects.create(confirmed=True, **kwargs)

            relation = Friend.objects.get(
                source_user=target_user,
                target_user=source_user
            )

            relation.confirmed = True
            relation.save()

        else:
            friend = Friend.objects.create(**kwargs)
        return friend

    def delete_remove_friend(self, instance):
        if self.are_friends(instance.source_user, instance.target_user):
            Friend.objects.get(source_user=instance.target_user, target_user=instance.source_user).delete()
        instance.delete()

    def is_pending_save(self, **kwargs):
        source_user = kwargs.get('source_user')
        target_user = kwargs.get('target_user')
        try:
            pending = Friend.objects.get(source_user=target_user, target_user=source_user, confirmed=False)
            if pending:
                pending.confirmed = True
                pending.save()
                return True
            else:
                return False
        except Friend.DoesNotExist:
            return False

    def is_pending(self, source_user, target_user):
        try:
            friend = Friend.objects.get(source_user=target_user, target_user=source_user, confirmed=False)
            if friend:
                return True
            else:
                return False
        except Friend.DoesNotExist:
            return False

class Friend(UUIDIdMixin):
    source_user = models.ForeignKey(Account, related_name="friend_source")
    target_user = models.ForeignKey(Account, related_name="friend")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    confirmed = models.BooleanField(default=False) # False = pending, True = both have POST'ed to each others friends list

    objects = FriendManager()

    class Meta:
        verbose_name = ('Account Friend')
        verbose_name_plural = ('Account Friends')
        unique_together = ('source_user', 'target_user')

    def __unicode__(self):
        return ("Friend id: %s (Source: %s Target: %s Confirmed: %s)" % (self.id, self.source_user, self.target_user, self.confirmed))

    def save(self, *args, **kwargs):
        if self.source_user == self.target_user:
            raise ValidationError("Users cannot be friends with themselves.")
        super(Friend, self).save(*args, **kwargs)

class Relationship(UUIDIdMixin):
    source_user = models.ForeignKey(Account, related_name="relationship_source")
    target_user = models.ForeignKey(Account, related_name="relationship_target")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    blocking = models.BooleanField(default=False)
    muting = models.BooleanField(default=False)
    marked_as_spam = models.BooleanField(default=False)
    notifications_enabled = models.BooleanField(default=False)

    class Meta:
        verbose_name = ('Account Relationship')
        verbose_name_plural = ('Account Relationships')
        unique_together = ('source_user', 'target_user')

    def __unicode__(self):
        return ("Relationship id: %s (Source: %s Target: %s)" % (self.id, self.source_user, self.target_user))
