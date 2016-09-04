from __future__ import unicode_literals
from django.apps import AppConfig

from activity.signals import action

class ActivityConfig(AppConfig):
    name = 'activity'

    def ready(self):
        from activity.actions import action_handler
        action.connect(action_handler)
