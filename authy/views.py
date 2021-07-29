from django import template
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from authy.forms import SignupForm, ChangePasswordForm, EditProfileForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.db.models import Sum

from authy.models import Profile
import uuid
from django.db import transaction
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.core.paginator import Paginator

from django.urls import resolve

import threading


class EmailThread(threading.Thread):

    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()

# Create your views here.
def home(request):
    template = "home.html"
    context = {}
    return render(request, template, context)

def SideNavInfo(request):
	user = request.user
	nav_profile = None

	if user.is_authenticated:
		nav_profile = Profile.objects.get(user=user)
	
	return {'nav_profile': nav_profile}


def UserProfile(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)
	template = loader.get_template('profile.html')
	context = {
		'profile':profile,

	}

	return HttpResponse(template.render(context, request))


def Signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			user = User.objects.create_user(username=username, email=email, password=password)
			user.is_active = False
			user.save()
			current_site = 'http://127.0.0.1:8000'
			email_subject = 'Active your Account'
			message = render_to_string('registration/activate.html',
                                   {
                                       'user': user,
                                       'domain': 'http://127.0.0.1:8000',
                                       'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                       'token': generate_token.make_token(user)
                                   }
                                   )
			email_message = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [email]
            )
			EmailThread(email_message).start()
			messages.add_message(request, messages.SUCCESS,
                            'account created succesfully')

             
			 
			return redirect('login')
	else:
		form = SignupForm()
	
	context = {
		'form':form,
	}

	return render(request, 'registration/signup.html', context)


@login_required
def PasswordChange(request):
	user = request.user
	if request.method == 'POST':
		form = ChangePasswordForm(request.POST)
		if form.is_valid():
			new_password = form.cleaned_data.get('new_password')
			user.set_password(new_password)
			user.save()
			update_session_auth_hash(request, user)
			return redirect('change_password_done')
	else:
		form = ChangePasswordForm(instance=user)

	context = {
		'form':form,
	}

	return render(request, 'registration/change_password.html', context)

def PasswordChangeDone(request):
	return render(request, 'registration/change_password_done.html')


@login_required
def EditProfile(request):
	user = request.user.id
	profile = Profile.objects.get(user__id=user)
	user_basic_info = User.objects.get(id=user)

	if request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES, instance=profile)
		if form.is_valid():
			profile.picture = form.cleaned_data.get('picture')
			profile.banner = form.cleaned_data.get('banner')
			user_basic_info.first_name = form.cleaned_data.get('first_name')
			user_basic_info.last_name = form.cleaned_data.get('last_name')
			profile.location = form.cleaned_data.get('location')
			profile.url = form.cleaned_data.get('url')
			profile.profile_info = form.cleaned_data.get('profile_info')
			profile.save()
			user_basic_info.save()
			return redirect('index')
	else:
		form = EditProfileForm(instance=profile)

	context = {
		'form':form,
	}

	return render(request, 'registration/edit_profile.html', context)


def activate(request,uidb64,token):
	try:
		uid =  urlsafe_base64_decode(uidb64).decode()
		user = User.objects.get(pk=uid)
	except Exception as identifier:
		user = None
	if user is not None and generate_token.check_token(user, token):
		user.is_active = True
		user.save()
		messages.add_message(request, messages.SUCCESS,'account activated successfully')
		return redirect('login')
	return render(request, 'registration/activate_failed.html', status=401)
