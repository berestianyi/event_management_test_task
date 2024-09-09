from rest_framework import serializers
from .models import Event, EventRegistration

from django.utils.translation import gettext as _


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'location', 'organizer']
        read_only_fields = ['organizer']


class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = ['id', 'user', 'event', 'registered_at']
        read_only_fields = ['registered_at', 'user']

    def create(self, validated_data):
        user = validated_data['user']
        event = validated_data['event']

        if EventRegistration.objects.filter(user=user, event=event).exists():
            raise serializers.ValidationError(_("You are already registered for this event."))

        return super().create(validated_data)
