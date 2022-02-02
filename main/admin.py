from django.contrib import admin

from main.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "bio"]
    search_fields = ["user"]
