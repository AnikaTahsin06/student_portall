from django.contrib import admin
from authy.models import Profile,Contact
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'token', 'verify','picture', 'created']

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Contact)