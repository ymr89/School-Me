from app.forms import LoginForm
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Login '/accounts/login/'
def login (request):
	# If already signed in, redirect to user home
	if request.user.is_authenticated():
		return HttpResponseRedirect('/userhome')
	form = LoginForm()
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = request.POST.get('username')
			password = request.POST.get('password')
			user = authenticate(username=username, password=password)
			# Sign in if user is successfully authenticated
			# Else display error message on login page
			if user is not None:
				auth_login(request, user)
				return redirect('/userhome/')
			else:
				messages.error(request, 'Invalid login or password')
		else:
			messages.error(request, 'Missing username or password')
	return render(request, 'app/login.html', {'form': form})

# Logout '/logout/'
@login_required
def logout(request):
	auth_logout(request)
	messages.success(request, 'Logout Successful')
	return redirect('/')