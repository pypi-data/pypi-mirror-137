from uuid import uuid4

from pubsub_event_store.serializers import EventDetailsSerializer


def create_event(adapter_name, body):
    event_id = uuid4()
    data = dict(
        event_id=event_id,
        adapter=adapter_name,
        data=body,
    )
    serializer = EventDetailsSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    event_details = serializer.save()
    return event_details.event_id
