from django.contrib import admin
from .models import PickupRequest

@admin.register(PickupRequest)
class PickupRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "pickup_date", "status")
    list_filter = ("status",)
    search_fields = ("user__username", "address")
