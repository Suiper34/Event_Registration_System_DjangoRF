from django.urls import path

from .views import (EventDetailView, EventListCreateView, MyRegistrationsView,
                    api_register, cancel_registration, register_event,
                    token_for_user, user_register, home)

app_name = 'events'

urlpatterns = [
    path('events/', EventListCreateView.as_view(), name='event-list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('events/<int:pk>/register/', register_event, name='event-register'),
    path('events/<int:pk>/cancel/', cancel_registration, name='event-cancel'),
    path('my-registrations/', MyRegistrationsView.as_view(),
         name='my-registrations'),

    # web registration
    path('accounts/register/', user_register, name='user-register'),
    path('', home, name='home'),

    # API signup and token-from-session endpoints
    path('api/register/', api_register, name='api-register'),
    path('api/token/', token_for_user, name='api-token-for-user'),
]
