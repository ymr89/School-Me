from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from app.forms import SignUpForm
from app.models import Organization, Profile, Board, Email_Token, Group
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User 


# Home/Landing '/'
def index(request):
	return render(request, 'app/home.html')

# Features '/more/'
def more(request):
	return render(request, 'app/more.html')

def contact(request):
	return render(request, 'app/contact.html')

# Sign up '/signup/'
def signup(request):
	# If already signed in, redirect to user home 
	if request.user.is_authenticated():
		return HttpResponseRedirect('/userhome/')
	form = SignUpForm()
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			organization = form.cleaned_data['organization']
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			# If organization does not already exist in DB, create a new organization and save to DB
			# else get existing organization to save to profile
			if not Organization.objects.filter(organization_name=organization).exists():
				new_organization = Organization(organization_name=organization)
				new_organization.save()
			else:
				new_organization = Organization.objects.get(organization_name=organization)
			profile_to_save = Profile(user=User.objects.create_user(username=username,
                                 							email=email,
                                 							password=password,
                                 							first_name=first_name,
                                 							last_name=last_name), 
							  user_organization=new_organization)
			profile_to_save.save()
			messages.success(request, 'Account Successfully Created')
			return redirect('/accounts/login/')
	return render(request, 'app/signup.html', {'form': form})

# Sign up w/ token '/signup/<token>/'
def signup_token(request, token):
	if not Email_Token.objects.filter(token=token).exists():
		messages.error('Invalid token.')
		return redirect('/')
	if request.user.is_authenticated():
		return HttpResponseRedirect('/userhome/')
	email_token = Email_Token.objects.get(token=token)
	# initialize email field with default email stored with token
	form = SignUpForm(initial={'email': email_token.email})
	# make email field readonly
	form.fields['email'].widget.attrs['readonly'] = True
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			organization = form.cleaned_data['organization']
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			# if submitted email does not match email stored with token, return error
			if email != email_token.email:
				messages.error(request, 'Invalid email address')
				return redirect('/' + token + '/signup/')
			# If organization does not already exist in DB, create a new organization and save to DB
			# else get existing organization to save to profile
			if not Organization.objects.filter(organization_name=organization).exists():
				new_organization = Organization(organization_name=organization)
				new_organization.save()
			else:
				new_organization = Organization.objects.get(organization_name=organization)
			profile_to_save = Profile(user=User.objects.create_user(username=username,
                                 							email=email,
                                 							password=password,
                                 							first_name=first_name,
                                 							last_name=last_name), 
							  		user_organization=new_organization)
			profile_to_save.save()
			board = email_token.board.board_name
			boardObj = Board.objects.get(board_name=board)
			profile_to_save.boards.add(boardObj)
			boardMemberGroup = Group.objects.get(name=board + ' member')
			profile_to_save.user.groups.add(boardMemberGroup)
			messages.success(request, 'Account Successfully Created')
			email_token.delete()
			return redirect('/accounts/login/')
	return render(request, 'app/signup_token.html', {'form': form, 'token': token})

