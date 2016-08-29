from django.conf.urls import include, url
from . import views

app_name = 'chat'
urlpatterns = [
    url(r'^conversation/(?P<chatroom_id>\d+)$', views.AccountViewSet.as_view()),
    url(r'^conversation/(?P<chatroom_id>\d+)/messages/(?P<message_id>\d+)$' view.MessageViewSet.as_view()),
]
