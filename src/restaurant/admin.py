from django.contrib import admin
from .models import Restaurant, Menu, Item
from django.contrib.admin import SimpleListFilter
from django.utils import timezone
from datetime import timedelta

class CreatedAtFilter(SimpleListFilter):
    title = 'Created At'
    parameter_name = 'created_at'

    def lookups(self, request, model_admin):
        return (
            ('last_24_hours', 'Last 24 Hours'),
            ('last_week', 'Last Week'),
            ('last_month', 'Last Month'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'last_24_hours':
            return queryset.filter(created_at__gte=timezone.now() - timedelta(days=1))
        elif value == 'last_week':
            return queryset.filter(created_at__gte=timezone.now() - timedelta(weeks=1))
        elif value == 'last_month':
            return queryset.filter(created_at__gte=timezone.now() - timedelta(weeks=4))
        return queryset

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ["id", "restaurant_name","slug", "address", "owner__username"]
    list_display_links = ["id", "restaurant_name"]
    search_fields = ["restaurant_name", "owner__username"]
    list_filter = [CreatedAtFilter,  "updated_at"]
    autocomplete_fields = ["owner"]

admin.site.register(Menu)
admin.site.register(Item)

