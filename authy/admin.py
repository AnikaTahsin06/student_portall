from django.contrib import admin
from authy.models import Profile
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'token', 'verify', 'created']

admin.site.register(Profile, ProfileAdmin)