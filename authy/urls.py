from django.urls import path
from authy.views import UserProfile, Signup, PasswordChange, PasswordChangeDone, EditProfile, activate,home

from django.contrib.auth import views as auth_Views 
#from . import views



urlpatterns = [
   	
    path('profile/edit', EditProfile, name='edit-profile'),
   	path('signup/', Signup, name='signup'),
   	path('home/', home, name='home'),
   	path('login/', auth_Views.LoginView.as_view(template_name='registration/login.html'), name='login'),
	path('activate/<uidb64>/<token>',  activate , name='activate'),
   	path('logout/', auth_Views.LogoutView.as_view(), {'next_page' : 'index'}, name='logout'),
   	path('changepassword/', PasswordChange, name='change_password'),
   	path('changepassword/done', PasswordChangeDone, name='change_password_done'),
   	path('passwordreset/', auth_Views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
   	path('passwordreset/done', auth_Views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
   	path('passwordreset/<uidb64>/<token>/', auth_Views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
   	path('passwordreset/complete/', auth_Views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

]