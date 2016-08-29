from django import forms
from django.contrib.auth.models import User, Group
from .models import Board
from django.utils.safestring import mark_safe


class SignUpForm(forms.Form):
	first_name = forms.CharField(label='First Name', max_length=30)
	last_name = forms.CharField(label='Last Name', max_length=30)
	organization = forms.CharField(label='School', max_length=30)
	username = forms.CharField(label='Username', max_length=30)
	email = forms.EmailField()
	password = forms.CharField(label='Password', max_length=30, widget=forms.PasswordInput)
	confirm_password = forms.CharField(label='Confirm Password', max_length=30, widget=forms.PasswordInput)

	# def __init__(self, *args, **kwargs):
	# 	super(SignUpForm, self).__init__(*args, **kwargs)
	# 	self.fields['password'].required = False
	# 	self.fields['confirm_password'].required = False

	def clean(self):
		password = self.cleaned_data.get('password')
		confirm_password = self.cleaned_data.get('confirm_password')
		username = self.cleaned_data.get('username')
		email = self.cleaned_data.get('email')
		if User.objects.filter(username=username).exists():
			self._errors['username'] = self.error_class(['Username is already in use'])
			raise forms.ValidationError(u'Username "%s" is already in use.' % username)
		if User.objects.filter(email=email).exists():
			self._errors['email'] = self.error_class(['Email is already in use'])
			raise forms.ValidationError(u'Email "%s" is already in use.' % email)
		if password and password != confirm_password:
			self._errors['confirm_password'] = self.error_class(['Passwords do not match'])
			raise forms.ValidationError("Passwords do not match")
		return self.cleaned_data


class LoginForm(forms.Form):
	username = forms.CharField(label='Username', max_length=30)
	password = forms.CharField(label='Password', max_length=30, widget=forms.PasswordInput)

class CreateBoardForm(forms.Form):
	board_name = forms.CharField(label="Board Name", max_length=30)
	CHOICES = (('0', 'Public'), ('1', 'Private'))
	board_privacy = forms.ChoiceField(initial=0, label='Privacy', choices=CHOICES, required=True)

	def clean(self):
		board_name = self.cleaned_data.get('board_name')
		if Board.objects.filter(board_name=board_name).exists():
			self._errors['board_name'] = self.error_class(['Board name is already taken'])
			raise forms.ValidationError(u'Board name "%s" is already taken.' % board_name)

class EditBoardForm(forms.Form):
	board_name = forms.CharField(label="New Name", max_length=30)

class CreateAnnouncementForm(forms.Form):
	description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'class':'form-control'}))
	end_date = forms.DateField(label='Expires', widget=forms.TextInput(attrs={'class':'datepicker form-control', 'id':'end_date_create'}))

class EditAnnouncementForm(forms.Form):
	description = forms.CharField(label='Edit Description', widget=forms.Textarea(attrs={'class':'form-control'}))
	end_date = forms.DateField(label='Expires', widget=forms.TextInput(attrs={'class':'datepicker form-control'}))

class FeedbackForm(forms.Form):
	CHOICES = (('0', 'Clarification'), ('1', 'Explanation'))
	title = forms.CharField(label='Title')
	feedbackType = forms.ChoiceField(initial=0, label='Type', choices=CHOICES, required=True)
	body = forms.CharField(label='Body', widget=forms.Textarea(attrs={'id':'form-body'}))
	tags = forms.CharField(label='Tags')
	#needed when file upload for a feedback post gets implemented
	#feedback_file = forms.FileField(label='File (Optional)', required=False, widget=forms.FileInput())

class DiscussionForm(forms.Form):
	title = forms.CharField(label='Title')
	body = forms.CharField(label='Body', widget=forms.Textarea(attrs={'id':'form-body'}))
	tags = forms.CharField(label='Tags')

class EditCommentForm(forms.Form):
 	comment = forms.CharField(widget=forms.Textarea)

class EditFeedbackForm(forms.Form):
	title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'class':'form-control'}))
	body = forms.CharField(label='Body', widget=forms.Textarea(attrs={'class':'form-control'}))
	tags = forms.CharField(label='Tags', widget=forms.TextInput(attrs={'class':'form-control'}))

class EditDiscussionForm(forms.Form):
	title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'class':'form-control'}))
	body = forms.CharField(label='Body', widget=forms.Textarea(attrs={'class':'form-control'}))
	tags = forms.CharField(label='Tags', widget=forms.TextInput(attrs={'class':'form-control'}))

class TagForm(forms.Form):
	tag = forms.CharField(label='Tag')

class FilterForm(forms.Form):
	POSTCHOICES = (('0', 'All'), ('1', 'Clarification'), ('2', 'Explanation'))
	postType = forms.ChoiceField(initial=0, label='Posts', choices=POSTCHOICES, required=False, widget=forms.Select(attrs={"onChange":'this.form.submit();'}))
	FILTERCHOICES = (('0', 'Most Recent'), ('1', 'Popularity'), ('2', 'Oldest'))
	filterType = forms.ChoiceField(initial=0, label='Filter By', choices=FILTERCHOICES, required=False, widget=forms.Select(attrs={"onChange":'this.form.submit();'}))

class FilterDiscussionForm(forms.Form):
	FILTERCHOICES = (('0', 'Most Recent'), ('1', 'Popularity'), ('2', 'Oldest'))
	filterType = forms.ChoiceField(initial=0, label='Filter By', choices=FILTERCHOICES, required=False, widget=forms.Select(attrs={"onChange":'this.form.submit();'}))

class TagForm(forms.Form):
	tag = forms.CharField(label='Tag')
	
class EditProfileForm(forms.Form):
	first = forms.CharField(label='First Name', required=False)
	last = forms.CharField(label='Last Name', required=False)
	organization = forms.CharField(label='School', required=False)
	email = forms.CharField(label='E-mail', required=False)

class UploadFileForm(forms.Form):
	file_file = forms.FileField(label='File', widget=forms.FileInput())
	name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'placeholder': 'Name your file'}))
	description = forms.CharField(label='Description', widget=forms.TextInput(attrs={'placeholder': 'Enter a short description for the file'}))
