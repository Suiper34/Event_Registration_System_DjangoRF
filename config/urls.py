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

    # API
    path('api/', include('events.urls')),
]
