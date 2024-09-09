from django.urls import path

from events.views import EventListCreateView, EventDetailView, EventRegistrationView

urlpatterns = [
    path('events/', EventListCreateView.as_view(), name='event_list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('events/register/', EventRegistrationView.as_view(), name='event_register'),
]
