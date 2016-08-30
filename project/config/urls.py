import os

from django.conf.urls import include, url, patterns
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_nested import routers

from oauth2_provider import views
from django.conf import settings

# Authentication views
from authentication.views import AccountViewSet
from authentication.views import CurrentUserView

# Chat views
from chat.views import RoomViewSet
from chat.views import MessageViewSet
from chat.views import NestedMessageViewSet

# creat router and register our viewsets with it.
router = routers.DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'room', RoomViewSet)

room_router = routers.NestedSimpleRouter(router, r'room', lookup='room')
room_router.register(r'messages', NestedMessageViewSet, base_name='room-messages')

'''
Include oauth2_provider urls one by one because "/applications" urls are not secure.
See this issue :  https://github.com/evonove/django-oauth-toolkit/issues/196
Waitting for fix in the meantime
'''
print(os.environ.get('DJANGO_SETTINGS_MODULE'))

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(room_router.urls)),
    url(r'^authorize/$', views.AuthorizationView.as_view(), name="authorize"),
    url(r'^token/$', views.TokenView.as_view(), name="token"),
    url(r'^revoke_token/$', views.RevokeTokenView.as_view(), name="revoke-token"),
    url(r'^me/', CurrentUserView.as_view(), name="whoami"),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Warning : the following lines are unsecure
if settings.DEBUG:
    # Application management views
    urlpatterns += [
        url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    ]
