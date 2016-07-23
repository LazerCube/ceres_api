import os

from django.conf.urls import include, url, patterns
from django.conf import settings
from django.conf.urls.static import static

from oauth2_provider import views
from django.conf import settings

"""
Include oauth2_provider urls one by one because "/applications" urls are not secure.
See this issue :  https://github.com/evonove/django-oauth-toolkit/issues/196
Waitting for fix in the meantime
"""
print(os.environ.get('DJANGO_SETTINGS_MODULE'))

urlpatterns = [
    url(r'^', include('authentication.urls')),
    url(r'^authorize/$', views.AuthorizationView.as_view(), name="authorize"),
    url(r'^token/$', views.TokenView.as_view(), name="token"),
    url(r'^revoke_token/$', views.RevokeTokenView.as_view(), name="revoke-token"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Warning : the following lines are unsecure
if settings.DEBUG:
    # Application management views
    urlpatterns += [
        url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    ]
