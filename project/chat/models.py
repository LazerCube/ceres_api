from __future__ import unicode_literals

from django.db import models
from authentication.models import Account

from django.contrib.contenttypes.models import ContentType, ContentTypeManager
from django.contrib.contenttypes.fields import GenericForeignKey

class RoomManager(models.Manager):
    def create(self, object, name, desc):
        '''Creates a new chat room and registers it to the calling object'''

        r = self.model(content_object=object, name=name, description=desc)
        r.save()
        return r

    def get_for_object(self, object):
        '''Try to get a room related to the object passed'''
        return self.get(content_type=ContentType.objects.get_for_model(object), object_id=object.pk)

    def get_or_create(self, object, name, desc):
        '''see if object exists if not create a room if none exists'''
        try:
            return self.get_for_object(object)
        except Room.DoesNotExist:
            return self.create(object, name, desc)

class Room(models.Model):
    name = models.CharField(max_length=64)
    content_type = models.ForeignKey(ContentType) #What kind of content is this related to
    object_id = models.PositiveIntegerField() # to which instace of the aforementioned object is this related
    content_object = GenericForeignKey('content_type','object_id') # use both up, USE THIS WHEN INSTANCING THE MODEL
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = RoomManager() # custom manager

    def __str__(self):
        return "Room ID:%d | Name:%s | Desc:%s" % (self.pk, self.name, self.description)

    def create_message(self, msg_type, sender, message):
        '''Function for adding messages into the chat room'''
        m = Message(room=self, msg_type=msg_type, author=sender, message=message)
        m.save()
        return m

    def say(self, sender, message):
        '''Says something into the chat'''
        return self.create_message('m', sender, message)

    def join(self, user):
        '''A user has joinned the chat'''
        return self.create_message('j', user)

    def leave(self, user):
        '''A user has left the chat'''
        return self.create_message('l', user)

    def messages(self, after_pk=None, after_date=None):
        '''List messages, after the given id or date'''
        m = Message.objects.filter(room=self)
        if after_pk:
            m = m.filter(pk__gt=after_pk)
        if after_date:
            m = m.filter(timestamp__gte=after_date)
        return m.order_by('pk')

    def last_message_id(self):
        '''Return last message sent to room'''
        m = Message.objects.filter(room=self).order_by('-pk')
        if m:
            return m[0].id
        else:
            return 0

    def message_num(self):
        '''Retuns number of messages in the room'''
        return Message.objects.filter(room=self).count()

    def __unicode__(self):
        #return 'Chat for %s %d' % (self.content_type, self.object_id)
        return "Room ID: %d | Name: %s | Desc: %s" % (self.pk, self.name, self.description)

    def save(self, *args, **kwargs):
        super(Room, self).save(*args, **kwargs)

MESSAGE_TYPE_CHOICES = (
    ('s','system'),
    ('a','action'),
    ('m', 'message'),
    ('j','join'),
    ('l','leave'),
    ('n','notification')
)

class Message(models.Model):
    '''A message that belongs to a chat room'''
    room = models.ForeignKey(Room)
    msg_type = models.CharField(max_length=1, choices=MESSAGE_TYPE_CHOICES)
    author = models.ForeignKey(Account, related_name='author', blank=True, null=True)
    message = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        '''Each message type has a special representation, return that representation.'''
        if self.msg_type == 's':
            return u'SYSTEM: %s' % self.message
        if self.msg_type == 'n':
            return u'NOTIFICATION: %s' % self.message
        elif self.msg_type == 'j':
            return 'JOIN: %s' % self.author
        elif self.msg_type == 'l':
            return 'LEAVE: %s' % self.author
        elif self.msg_type == 'a':
            return 'ACTION: %s > %s' % (self.author, self.message)
        return self.message
