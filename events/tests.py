from datetime import datetime, timedelta, timezone

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import Event, Registration

User = get_user_model()


class EventAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # create users
        self.user = User.objects.create_user(
            username='user1', password='pass123')
        self.organizer = User.objects.create_user(
            username='org1', password='pass123', is_staff=True)

        # create an event with capacity 1
        now = datetime.now(timezone.utc)
        self.event = Event.objects.create(
            title='Test Event',
            description='desc',
            location='online',
            start_time=now,
            end_time=now + timedelta(hours=1),
            capacity=1,
            created_by=self.organizer
        )

    def test_list_events(self):
        url: str = reverse('event-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.json(), list))

    def test_register_and_cancel_flow(self):
        register_url: str = reverse(
            'event-register', kwargs={'pk': self.event.pk})

        # unauthenticated user cannot register
        response = self.client.post(register_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # authenticate and register
        self.client.login(username='user1', password='pass123')
        response = self.client.post(register_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Registration.objects.filter(
            user=self.user, event=self.event).exists())

        # prevent duplicate registration
        response_2 = self.client.post(register_url)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)

        # cancel registration
        cancel_url: str = reverse('event-cancel', kwargs={'pk': self.event.pk})
        response_3 = self.client.delete(cancel_url)
        self.assertEqual(response_3.status_code, status.HTTP_200_OK)
        self.assertFalse(Registration.objects.filter(
            user=self.user, event=self.event).exists())

    def test_event_full(self):
        # fill event with another user
        another_user = User.objects.create_user(
            username='user2', password='pass123')
        Registration.objects.create(user=another_user, event=self.event)

        self.client.login(username='user1', password='pass123')
        register_url = reverse('event-register', kwargs={'pk': self.event.pk})
        response = self.client.post(register_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Event is full', response.json().get('error', ''))
