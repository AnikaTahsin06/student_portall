from django.contrib import admin
 
from authy.models import Profile,Contact,teacherprofile
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user',  'location', 'profile_info', 'user_type', 'picture', 'created']

class TeacherAdmin(admin.ModelAdmin):
     list_display = ['id', 'bio','topic','mobile','url1' ,'user_type']

class ContactAdmin(admin.ModelAdmin):
    list_display = ['name','email','feedback']

admin.site.site_header = 'BrainAxis Admin Panel'
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(teacherprofile, TeacherAdmin)
