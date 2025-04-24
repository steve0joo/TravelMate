from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount

class SocialAccountInline(admin.TabularInline):
    model = SocialAccount
    extra = 0
    can_delete = False

class CustomUserAdmin(BaseUserAdmin):
    inlines = [SocialAccountInline]
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active')

# Safely unregister and re-register
if admin.site.is_registered(User):
    admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)