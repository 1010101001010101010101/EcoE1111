from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "organization", "role")
    search_fields = ("user__username", "organization__name", "role")
