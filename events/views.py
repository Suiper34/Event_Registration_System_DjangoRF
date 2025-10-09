import logging
from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.template import TemplateDoesNotExist
from django.urls import reverse
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Event, Registration
from .permissions import IsOrganizerOrReadOnly
from .serializers import EventSerializer, RegistrationSerializer

logger = logging.getLogger(__name__)

User = get_user_model()

year: int = datetime.now().year


def home(request):
    """
    Render the project index page. If index.html is missing, render 404.html
    """

    try:
        return render(request, 'index.html', {'year': year})

    except TemplateDoesNotExist:
        return render(request, '404.html', {'short_code': None}, status=200)


class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all().order_by('-start_time')
    serializer_class = EventSerializer
    permission_classes = [IsOrganizerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# Event detail
class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


# register for event
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def register_event(request, pk: int):
    """
    Attempt to register the authenticated user for event `id`.
    Uses a transaction and handles race conditions and duplicate registrations.
    """
    event = get_object_or_404(Event, pk=pk)

    if event.spots_left <= 0:
        return Response({'error': 'Event is full'},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        with transaction.atomic():
            # refresh to reduce race window
            event = Event.objects.select_for_update().get(pk=event.pk)
            if event.spots_left <= 0:
                return Response({'error': 'Event is full!'},
                                status=status.HTTP_400_BAD_REQUEST)

            reg, created = Registration.objects.get_or_create(
                user=request.user, event=event)
            if not created:
                return Response({'error': 'Already registered!'},
                                status=status.HTTP_400_BAD_REQUEST)

            serializer = RegistrationSerializer(reg)
            logger.info('User %s registered for event %s',
                        request.user, event.pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    except IntegrityError as ie:
        logger.exception(
            'Integrity error when registering user %s for event %s: %s',
            request.user, pk, ie)
        return Response({'error': 'Registration failed'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        logger.exception(
            'Unexpected error registering for event %s: %s', pk, e)
        return Response({'error': 'Server error'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# cancel registration
@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def cancel_registration(request, pk: int):
    """
    Cancel the authenticated user's registration for event `id`.
    """
    try:
        reg = Registration.objects.get(user=request.user, event_id=pk)
        reg.delete()
        logger.info('User %s cancelled registration for event %s',
                    request.user, pk)
        return Response({'message': 'Registration cancelled!'},
                        status=status.HTTP_200_OK)
    except Registration.DoesNotExist:
        return Response({'error': 'Not registered!'},
                        status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.exception(
            'Error cancelling registration for user %s event %s: %s',
            request.user, pk, e)
        return Response({'error': 'Server error!'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# View user’s registrations
class MyRegistrationsView(generics.ListAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Registration.objects.filter(
            user=self.request.user).select_related('event')


def user_register(request):
    """
    Web registration: renders register.html template  and creates a user.

    After successful signup redirect user to the DRF login page (session auth).
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('rest_framework:login'))
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def api_register(request):
    """
    API registration: accepts JSON body with 'username' and 'password' and or
    email.

    Returns token on success.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')

    if not username or not password:
        return Response({'error': 'username and password required'},
                        status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'username already exists'},
                        status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(
        username=username, password=password, email=email)
    token, _ = Token.objects.get_or_create(user=user)
    return Response(
        {'username': user.username, 'token': token.key},
        status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def token_for_user(request):
    """
    Return the token for the currently authenticated user.

    Useful when using the browsable API / session login and you want the
    user's token.
    """
    token, _ = Token.objects.get_or_create(user=request.user)
    return Response({'token': token.key})
