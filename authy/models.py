from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save

from PIL import Image
from django.conf import settings
import os

def user_directory_path_profile(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    profile_pic_name = 'user_{0}/profile.jpg'.format(instance.user.id)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)

    if os.path.exists(full_path):
    	os.remove(full_path)

    return profile_pic_name

def user_directory_path_banner(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    banner_pic_name = 'user_{0}/banner.jpg'.format(instance.user.id)
    full_path = os.path.join(settings.MEDIA_ROOT, banner_pic_name)

    if os.path.exists(full_path):
    	os.remove(full_path)

    return banner_pic_name

# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	token = models.CharField(max_length=150, default="")
	verify = models.BooleanField(default=False)
	location = models.CharField(max_length=50, null=True, blank=True)
	topic = models.CharField(max_length=50, null=True, blank=True)
	mobile = models.CharField(max_length=50, null=True, blank=True)
	url = models.CharField(max_length=80, null=True, blank=True)
	url1 = models.CharField(max_length=80, null=True, blank=True)
	profile_info = models.TextField(max_length=150, null=True, blank=True)
	plans = models.TextField(max_length=150, null=True, blank=True)
	created = models.DateField(auto_now_add=True)
	picture = models.ImageField(upload_to=user_directory_path_profile, blank=True, null=True, verbose_name='Picture')
	banner = models.ImageField(upload_to=user_directory_path_banner, blank=True, null=True, verbose_name='Banner')

	Nonee = 'None'
	month1 = '6 Months'
	month2 = '12 Months'
	month3 = '18 Months'
	month4 = '24 Months'
	last = 'More than 2 years of experience'

	experience = [
		(Nonee, 'None'),
		(month1, '6 Months'),
		(month2, '12 Months'),
		(month3, '18 Months'),
		(month4, '24 Months'),
		(last, 'More than 2 years of experience'),
	]


	teacher = 'teacher'
	student = 'student'
	user_types = [
        (teacher, 'teacher'),
        (student, 'student'),
    ]
	user_type = models.CharField(max_length=50, choices=user_types, default=student)

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		SIZE = 250, 250

		if self.picture:
			pic = Image.open(self.picture.path)
			pic.thumbnail(SIZE, Image.LANCZOS)
			pic.save(self.picture.path)


	def __str__(self):
		return self.user.username

class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    feedback = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home')
		

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

def save_user_profile(sender, instance,**kwargs):
	instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)