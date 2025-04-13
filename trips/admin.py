from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'message')
    list_filter = ('created_at', 'user')
    search_fields = ('message',)
