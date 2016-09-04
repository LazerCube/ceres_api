from __future__ import unicode_literals

from django.db import models
from django.db.models import Q

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.timesince import timesince as djtimesince
from collections import defaultdict

from core.mixins import UUIDIdMixin

class ActivityManager(models.Manager):

    def public(self, *args, **kwargs):
        '''Returns public actions'''
        kwargs['public'] = True
        return self.filter(*args, **kwargs)

    def actor(self, obj, **kwargs):
        ctype  = ContentType.objects.get_for_model(obj)
        return self.public(actor_object_id=obj.pk,
                            actor_content_type=ctype , **kwargs)

    def target(self, obj, **kwargs):
        ctype  = ContentType.objects.get_for_model(obj)
        return self.public(target_object_id=obj.pk,
                            target_content_type=ctype , **kwargs)

    def action_object(self, obj, **kwargs):
        ctype  = ContentType.objects.get_for_model(obj)
        return self.public(action_object_object_id=obj.pk,
                            action_object_content_type=ctype , **kwargs)

    def any(self, obj, **kwargs):
        ctype = ContentType.objects.get_for_model(obj)
        return self.public(
            Q(
                actor_content_type=ctype,
                actor_object_id=obj.pk,
            ) | Q(
                target_content_type=ctype,
                target_object_id=obj.pk,
            ) | Q(
                action_object_content_type=ctype,
                action_object_object_id=obj.pk,
            ), **kwargs)

    def user(self, obj, **kwargs):
        q = Q()
        qs = self.public()

        if not obj:
            return qs.none()

        actors_by_content_type = defaultdict(lambda: [])
        others_by_content_type = defaultdict(lambda: [])

        #option to get user activity, non object items.
        if kwargs.pop('with_user_activity', False):
            object_content_type = ContentType.objects.get_for_model(obj)
            actors_by_content_type[object_content_type.id].append(obj.pk)

        if len(actors_by_content_type) + len(others_by_content_type) == 0:
            return qs.none()

        for content_type_id, object_ids in actors_by_content_type.items():
            q = q | Q(
                actor_content_type=content_type_id,
                actor_object_id__in=object_ids,
            )
        for content_type_id, object_ids in others_by_content_type.items():
            q = q | Q(
                target_content_type=content_type_id,
                target_object_id__in=object_ids,
            ) | Q(
                action_object_content_type=content_type_id,
                action_object_object_id__in=object_ids,
            )
        return qs.filter(q, **kwargs)

VERB_TYPE_CHOICES = (
    ('add'),
    ('delete'),
    ('invite'),
    ('join'),
    ('leave'),
    ('like'),
    ('unlike'),
    ('request-friend'),
    ('remove-friend'),
    ('save'),
    ('update')
)

class Activity(UUIDIdMixin):
    '''
    Generalized Format::
        <actor> <verb> <time>
        <actor> <verb> <target> <time>
        <actor> <verb> <action_object> <target> <time>
    Examples::
        <lazer> <Logged in> <1 minute ago>
        <lazer> <commented on> <lazer-snorlax> <2 hours ago>
        <snorlax> <started follow> <lazer> <8 minutes ago>
        <snorlax> <deleted> <message 2> on <lazer-snorlax> <about 2 hours ago>
    '''
    actor_content_type = models.ForeignKey(ContentType, related_name='actor')
    actor_object_id = models.UUIDField()
    actor = GenericForeignKey('actor_content_type', 'actor_object_id') # Who did it (what object)

    verb = models.CharField(max_length=255) # What did they do?
    description = models.TextField(blank=True, null=True)

    target_content_type = models.ForeignKey(ContentType, blank=True, null=True, related_name='target')

    target_object_id = models.UUIDField(blank=True, null=True)
    target = GenericForeignKey('target_content_type', 'target_object_id') # What did they do it on? (object eg chatroom)

    action_object_content_type = models.ForeignKey(ContentType, blank=True, null=True, related_name='action_object')
    action_object_object_id = models.UUIDField(blank=True, null=True,)
    action_object = GenericForeignKey('action_object_content_type','action_object_object_id') # What part did they do it on

    public = models.BooleanField(default=True) # Can other people see it?
    timestamp = models.DateTimeField(auto_now=True, editable=False) # Time they did it at

    objects = ActivityManager()

    def __unicode__(self):
        ctx = {
            'actor': self.actor,
            'verb': self.verb,
            'action_object': self.action_object,
            'target': self.target,
            'timesince': self.timesince()
        }
        if self.target:
            if self.action_object:
                return ('%(actor)s %(verb)s %(action_object)s on %(target)s %(timesince)s ago') % ctx
            return ('%(actor)s %(verb)s %(target)s %(timesince)s ago') % ctx
        if self.action_object:
            return ('%(actor)s %(verb)s %(action_object)s %(timesince)s ago') % ctx
        return ('%(actor)s %(verb)s %(timesince)s ago') % ctx

    def timesince(self, now=None):
        return djtimesince(self.timestamp, now).encode('utf8').replace(b'\xc2\xa0', b' ').decode('utf8')
