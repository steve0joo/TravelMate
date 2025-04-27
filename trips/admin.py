from django.contrib import admin
from .models import Trip, PackingItem, Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'message')
    list_filter = ('created_at', 'user')
    search_fields = ('message',)


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'destination', 'start_date', 'end_date', 'trip_type', 'is_public')
    search_fields = ('name', 'destination', 'user__username')
    list_filter = ('trip_type', 'start_date', 'end_date', 'is_public')

    # Organize fields better
    fieldsets = (
        ('Trip Details', {
            'fields': ('user', 'name', 'destination', 'start_date', 'end_date', 'trip_type')
        }),
        ('Visibility', {
            'fields': ('is_public', 'share_token')
        }),
    )

    # Make share_token readonly because it should not be manually edited
    readonly_fields = ('share_token',)


@admin.register(PackingItem)
class PackingItemAdmin(admin.ModelAdmin):
    list_display = ('trip', 'name', 'is_packed')
    search_fields = ('trip__name', 'name')
