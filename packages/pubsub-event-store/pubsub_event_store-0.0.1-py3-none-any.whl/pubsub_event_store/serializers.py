from rest_framework import serializers

from pubsub_event_store.models import EventDetails


class EventDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventDetails
        fields = (
            "event_id",
            "adapter",
            "status",
            "data",
            "result",
            "error",
        )
