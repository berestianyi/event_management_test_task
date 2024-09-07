from rest_framework import generics, permissions
from .models import Event
from .serializers import EventSerializer


class EventListCreateView(generics.ListCreateAPIView):
    """
    Handles the listing and creation of events.

    GET: Retrieves a list of all events.
    POST: Creates a new event.

    The `perform_create` method sets the `organizer` field of the event
    to the currently authenticated user.

    Permissions:
        - Allows unauthenticated users to view the list of events.
        - Only authenticated users can create events.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
        Handles the retrieval, update, and deletion of a single event.

        GET: Retrieves a single event by its ID.
        PUT/PATCH: Updates the details of the specified event.
        DELETE: Deletes the specified event.

        The `perform_update` method ensures that the `organizer` field remains
        the same during an update.

        Permissions:
            - Allows unauthenticated users to retrieve event details.
            - Only authenticated users can update or delete events.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def perform_update(self, serializer):
        serializer.save(organizer=self.request.user)
