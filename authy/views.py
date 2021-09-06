from django import forms, template
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from django.views.generic import CreateView
from authy.forms import SignupForm, ChangePasswordForm, EditProfileForm,TeacherUserform,TeacherProfileInfoForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.views.generic import TemplateView
from classroom.models import Course, Category
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.db.models import Sum

from authy.models import Profile, Contact
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
	categories = Category.objects.all()
	course = Course.objects.all()
	#teachers = Profile.objects.all()
	teachers = Profile.objects.filter(  user_type='teacher')
	context = {
		'categories': categories,
		'course': course,
		'teachers': teachers,
	}
	return render(request, template, context)

def about(request):
	template = "about.html"
	teachers = Profile.objects.filter(  user_type='teacher')
	context = {
		'teachers':teachers,
	}
	return render(request, template, context)

class ContactView(CreateView):
    model = Contact
    fields = '__all__'
    template_name = 'registration/contact.html'

#views for search functionality
class Search(TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results = Course.objects.filter( Q(title__icontains=kw) )
        results2 = Category.objects.filter( Q(title__icontains=kw) )
        context["results"] = results
        context["results2"] = results2
        return context



# def Categories(request):
# 	categories = Category.objects.all()

# 	context = {
# 		'categories': categories
# 	}
# 	return render(request, 'classroom/categories.html', context)

# def CategoryCourses(request, category_slug):
# 	category = get_object_or_404(Category, slug=category_slug)
# 	courses = Course.objects.filter(category=category)

# 	context = {
# 		'category': category,
# 		'courses': courses,
# 	}
# 	return render(request, 'classroom/categorycourses.html', context)

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
                            'Account created succesfully.Please verify your account before login!')
			
			

             
			 
			return redirect('login')
	else:
		form = SignupForm()
	
	context = {
		'form':form,
	}

	return render(request, 'registration/signup.html', context)

def activate(request,uidb64,token):
	try:
		uid =  urlsafe_base64_decode(uidb64).decode()
		user = User.objects.get(pk=uid)
	except Exception as identifier:
		user = None
	if user is not None and generate_token.check_token(user, token):
		user.is_active = True
		user.save()
		messages.success(request, 'Account activated successfully.Now you can login!')
		return redirect('login')
	else:
		messages.warning(request, "activation link is invalid")
		return redirect('signup')
	#return render(request, 'registration/activate_failed.html', status=401)


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

def register(request):
	if request.method == 'POST':
		user_form = SignupForm(request.POST)
		if user_form.is_valid():
			username = user_form.cleaned_data.get('username')
			email = user_form.cleaned_data.get('email')
			password = user_form.cleaned_data.get('password')
			User.objects.create_user(username=username, email=email, password=password)
			return redirect('teacherinfo')
	else:
		user_form = SignupForm()
	
	context = {
		'user_form':user_form,
	}

	return render(request, 'registration/registration.html', context)

def teacherinfo(request):
	user = request.user.id
	profile = Profile.objects.get(user__id=user)
	print(profile)
	user_basic_info = User.objects.get(id=user)

	if request.method == 'POST':
		teacherform = EditProfileForm(request.POST, request.FILES, instance=profile)
		if teacherform.is_valid():
			profile.picture = teacherform.cleaned_data.get('picture')
			profile.banner = teacherform.cleaned_data.get('banner')
			user_basic_info.first_name = teacherform.cleaned_data.get('first_name')
			user_basic_info.last_name = teacherform.cleaned_data.get('last_name')
			profile.location = teacherform.cleaned_data.get('location')
			profile.url = teacherform.cleaned_data.get('url')
			profile.profile_info = teacherform.cleaned_data.get('profile_info')
			profile.save()
			user_basic_info.save()
			return redirect('home')
	else:
		teacherform = EditProfileForm(instance=profile)

	context = {
		'teacherform':teacherform,
	}

	return render(request, 'registration/edit_profile.html', context)


