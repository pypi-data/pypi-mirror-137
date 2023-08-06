from django.contrib import admin

from pubsub_event_store.models import EventDetails


class EventDetailsAdmin(admin.ModelAdmin):
    list_display = ("event_id", "adapter", "status", "data", "result", "error")
    search_fields = (
        "event_id",
        "adapter",
    )
    list_filter = (
        "status",
        "adapter",
        "created_at",
    )
    date_hierarchy = "created_at"
    readonly_fields = ("event_id", "adapter", "status", "data", "result", "error")


admin.site.register(EventDetails, EventDetailsAdmin)
