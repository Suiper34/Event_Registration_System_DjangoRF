import importlib

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),

    # browsable API session login/logout (DRF)
    path('api-auth/', include('rest_framework.urls',
                              namespace='rest_framework')),

    # token auth endpoint (POST username & password -> returns token)
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]

try:
    importlib.import_module('api.urls')
    urlpatterns.append(path('api/', include('api.urls')))
except ModuleNotFoundError:
    # expose events API under /api/ if no api app
    urlpatterns.append(path('api/', include('events.urls')))

# site root point to the events app
urlpatterns.append(path('', include('events.urls')))

# customize admin titles
admin.site.site_header = getattr(
    settings, 'ADMIN_SITE_TITLE', 'E.R.S Admins')
admin.site.site_title = getattr(
    settings, 'ADMIN_SITE_TITLE', 'E.R.S Admins')
admin.site.index_title = getattr(
    settings, 'ADMIN_INDEX_TITLE', 'JhapTech Administration')
