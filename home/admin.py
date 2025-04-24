from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register the built-in User model
admin.site.register(User, UserAdmin)

# Optionally register EmailAddress if not already done by allauth
try:
    from allauth.account.models import EmailAddress
    from allauth.account.admin import EmailAddressAdmin
    admin.site.register(EmailAddress, EmailAddressAdmin)
except admin.sites.AlreadyRegistered:
    pass