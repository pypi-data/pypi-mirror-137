from django.db import models
from model_utils import Choices


EVENT_STATUS_CHOICES = Choices("PENDING", "FAILED", "SUCCESS")


class EventDetails(models.Model):
    event_id = models.UUIDField(primary_key=True, unique=True)
    adapter = models.CharField(max_length=30)
    status = models.CharField(
        max_length=20,
        choices=EVENT_STATUS_CHOICES,
        default=EVENT_STATUS_CHOICES.PENDING,
    )
    data = models.JSONField(default=dict, null=True, blank=True)
    result = models.TextField(null=True, blank=True)
    error = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
