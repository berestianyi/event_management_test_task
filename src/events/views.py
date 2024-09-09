from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from rest_framework import generics, permissions, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import EventFilter
from .models import Event
from .serializers import EventSerializer, EventRegistrationSerializer
from .tasks import send_registration_email


from django.utils.translation import gettext as _


class EventListCreateView(generics.ListCreateAPIView):
    """
    Handles the listing and creation of events.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Event.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = EventFilter
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    @extend_schema(
        description='Retrieve a list of all available events. Supports filtering and searching.\n',
        responses={
            200: OpenApiResponse(response=EventSerializer(many=True), description="Successful operation."),
            400: OpenApiResponse(description="Bad request."),
        }
    )
    def get(self, request, *args, **kwargs):
        """Get a list of all events."""
        return super().get(request, *args, **kwargs)

    @extend_schema(
        description="Create a new event. The current authenticated user is set as the organizer.",
        request=EventSerializer,
        responses={
            201: EventSerializer,
            400: OpenApiResponse(description="Invalid data provided."),
        }
    )
    def post(self, request, *args, **kwargs):
        """Create a new event."""
        return super().post(request, *args, **kwargs)


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles the retrieval, update, and deletion of a single event.


    Methods:
        - GET: Retrieves details of a specific event using its ID.
        - PUT/PATCH: Updates the details of the specified event.
        - DELETE: Deletes the specified event.


    Permissions:
        - Unauthenticated users: Can retrieve event details (GET).
        - Authenticated users: Can update or delete events (PUT, PATCH, DELETE).


    Behavior:
        - In the `perform_update` method, the organizer of the event cannot be changed during an update. The organizer will remain the same as initially assigned.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def perform_update(self, serializer):
        serializer.save(organizer=self.request.user)


class EventRegistrationView(generics.CreateAPIView):
    """
    Handles user registration for an event.


    Methods:
        - POST: Registers the currently authenticated user for the specified event.


    Permissions:
        - Only authenticated users can register for an event (POST).


    Request Data:
        - The POST request must include an `event` field, which represents the event's ID that the user wishes to register for.

        Example:
        {
            "event": int (event_id)
        }

    Behavior:
        - Upon successful registration, an email is sent to the user to confirm their registration using `send_registration_email`.

    """
    serializer_class = EventRegistrationSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=EventRegistrationSerializer,
        responses={
            201: EventRegistrationSerializer,
            400: OpenApiResponse(description="Invalid request or data."),
            404: OpenApiResponse(description="Event not found."),
        },
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        event_id = request.data.get('event')

        if not event_id:
            return Response({'error': _('Event ID is required.')}, status=status.HTTP_400_BAD_REQUEST)

        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({'error': _('Event not found')}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data={'user': user.id, 'event': event.id})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(user=user)

        send_registration_email.delay(user.email, event.title)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

