from django.contrib.contenttypes.models import ContentType
from django.utils.six import text_type
from django.dispatch import receiver
from activity.signals import action

from activity.models import Activity

@receiver(action)
def action_handler(verb, **kwargs):
    kwargs.pop('signal', None)
    actor = kwargs.pop('sender')

    if hasattr(verb, '_proxy____args'):
        verb = verb._proxy____args[0]

    newaction = Activity.objects.create(
        actor_content_type=ContentType.objects.get_for_model(actor),
        actor_object_id=actor.pk,
        verb=text_type(verb),
        public=bool(kwargs.pop('public', True)),
        description=kwargs.pop('description', None),
    )

    for opt in ('target', 'action_object'):
        obj = kwargs.pop(opt, None)
        if obj is not None:
            setattr(newaction, '%s_object_id' % opt, obj.pk)
            setattr(newaction, '%s_content_type' % opt,
                    ContentType.objects.get_for_model(obj))

    newaction.save()
    return newaction
