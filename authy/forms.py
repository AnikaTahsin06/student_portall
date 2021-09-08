from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from authy.models import Profile, teacherprofile

def ForbiddenUsers(value):
	forbidden_users = ['admin', 'css', 'js', 'authenticate', 'login', 'logout', 'administrator', 'root',
	'email', 'user', 'join', 'sql', 'static', 'python', 'delete']
	if value.lower() in forbidden_users:
		raise ValidationError('Invalid name for user, this is a reserverd word.')

def InvalidUser(value):
	if '@' in value or '+' in value or '-' in value:
		raise ValidationError('This is an Invalid user, Do not user these chars: @ , - , + ')

def UniqueEmail(value):
	if User.objects.filter(email__iexact=value).exists():
		raise ValidationError('User with this email already exists.')

def UniqueUser(value):
	if User.objects.filter(username__iexact=value).exists():
		raise ValidationError('User with this username already exists.')

class SignupForm(forms.ModelForm):
	username = forms.CharField(widget=forms.TextInput(), max_length=30, required=True,)
	email = forms.CharField(widget=forms.EmailInput(), max_length=100, required=True,)
	password = forms.CharField(widget=forms.PasswordInput())
	confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True, label="Confirm your password.")

	class Meta:

		model = User
		fields = ('username', 'email', 'password')

	def __init__(self, *args, **kwargs):
		super(SignupForm, self).__init__(*args, **kwargs)
		self.fields['username'].validators.append(ForbiddenUsers)
		self.fields['username'].validators.append(InvalidUser)
		self.fields['username'].validators.append(UniqueUser)
		self.fields['email'].validators.append(UniqueEmail)

	def clean(self):
		super(SignupForm, self).clean()
		password = self.cleaned_data.get('password')
		confirm_password = self.cleaned_data.get('confirm_password')

		if password != confirm_password:
			self._errors['password'] = self.error_class(['Passwords do not match. Try again'])
		return self.cleaned_data

class ChangePasswordForm(forms.ModelForm):
	id = forms.CharField(widget=forms.HiddenInput())
	old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium'}), label="Old password", required=True)
	new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium'}), label="New password", required=True)
	confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium'}), label="Confirm new password", required=True)

	class Meta:
		model = User
		fields = ('id', 'old_password', 'new_password', 'confirm_password')

	def clean(self):
		super(ChangePasswordForm, self).clean()
		id = self.cleaned_data.get('id')
		old_password = self.cleaned_data.get('old_password')
		new_password = self.cleaned_data.get('new_password')
		confirm_password = self.cleaned_data.get('confirm_password')
		user = User.objects.get(pk=id)
		if not user.check_password(old_password):
			self._errors['old_password'] =self.error_class(['Old password do not match.'])
		if new_password != confirm_password:
			self._errors['new_password'] =self.error_class(['Passwords do not match.'])
		return self.cleaned_data

#Teacher form
class TeacherUserform(UserCreationForm):
    email = forms.EmailField()

    class Meta():
        model = User
        fields = ('username', 'email', 'password1', 'password2')

        labels = {
            'password1':'Password',
            'password2':'Confirm Password'
        }
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

class UserProfileInfoForm(forms.ModelForm):
	bio = forms.CharField(required=False)
	topic = forms.CharField(widget=forms.TextInput(), max_length=50, required=False)
	mobile = forms.CharField(widget=forms.TextInput(), max_length=50, required=False)
	url = forms.URLField(widget=forms.TextInput(), max_length=60, required=False)
	url1 = forms.URLField(widget=forms.TextInput(), max_length=60, required=False)
	plans = forms.CharField(widget=forms.TextInput(), max_length=260, required=False)

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
	experienc = forms.ChoiceField(required=True, choices=experience)
	teacher = 'teacher'
	user_types = [
         
        (teacher, 'teacher'),
    ]
	user_type = forms.ChoiceField(required=True, choices=user_types)
	class Meta():
		model = teacherprofile
		fields = ('bio', 'profile_pic', 'topic', 'mobile', 'url', 'url1', 'plans', 'experienc', 'user_type')


# class TeacherProfileInfoForm(forms.ModelForm):
# 	topic = forms.CharField(widget=forms.TextInput(), max_length=50, required=False)
# 	mobile = forms.CharField(widget=forms.TextInput(), max_length=50, required=False)
# 	url = forms.URLField(widget=forms.TextInput(), max_length=60, required=False)
# 	url1 = forms.URLField(widget=forms.TextInput(), max_length=60, required=False)
# 	plans = forms.CharField(widget=forms.TextInput(), max_length=260, required=False)

# 	Nonee = 'None'
# 	month1 = '6 Months'
# 	month2 = '12 Months'
# 	month3 = '18 Months'
# 	month4 = '24 Months'
# 	last = 'More than 2 years of experience'

# 	experience = [
# 		(Nonee, 'None'),
# 		(month1, '6 Months'),
# 		(month2, '12 Months'),
# 		(month3, '18 Months'),
# 		(month4, '24 Months'),
# 		(last, 'More than 2 years of experience'),
# 	]
# 	experienc = forms.ChoiceField(required=True, choices=experience)


# 	teacher = 'teacher'
# 	user_types = [
#         (teacher, 'teacher'),
#     ]
# 	user_type = forms.ChoiceField(required=True, choices=user_types)
# 	class Meta():
# 		model = Profile
# 		fields = ('topic', 'mobile', 'url', 'url1', 'plans', 'experienc', 'user_type')

class EditProfileForm(forms.ModelForm):
	first_name = forms.CharField(widget=forms.TextInput(), max_length=50, required=False)
	last_name = forms.CharField(widget=forms.TextInput(), max_length=50, required=False)
	picture = forms.ImageField(required=False)
	banner = forms.ImageField(required=False)
	location = forms.CharField(widget=forms.TextInput(), max_length=25, required=False)
	url = forms.URLField(widget=forms.TextInput(), max_length=60, required=False)
	profile_info = forms.CharField(widget=forms.TextInput(), max_length=260, required=False)
	teacher = 'teacher'
	student = 'student'
	user_types = [
        (teacher, 'teacher'),
        (student, 'student'),
    ]
	user_type = forms.ChoiceField(required=True, choices=user_types)
	class Meta:
		model = Profile
		fields = ('picture', 'banner', 'first_name', 'last_name', 'location', 'url', 'profile_info', 'user_type')






