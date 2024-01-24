from django.contrib import admin

from ..models import RequestModel


@admin.register(RequestModel)
class RequestAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "email",
        "short_message",
        "phone",
        "ip_address",
        "created_at",
    )
    list_display_links = ("short_message",)
    ordering = RequestModel._meta.ordering
    search_fields = ["message", "created_at", "email", "phone", "ip_address"]
    date_hierarchy = "created_at"
