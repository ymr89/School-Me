from app.forms import CreateAnnouncementForm, EditAnnouncementForm, EditBoardForm
from app.models import Announcement, Board, Email_Token, Group, Profile
from app.views.search import get_query
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from hashlib import sha1

#Setting this flag true sends emails out
SEND_EMAILS = True

# Board Settings - access board settings as admin '/settings/<board>/'
# Parameters 
# - board: board name
@login_required
def board_settings(request, board):
	boardObj = Board.objects.get(board_name=board)
	boardAdmin = Group.objects.get(name=board + ' admin')
	boardMember = Group.objects.get(name=board + ' member')
	if not request.user.groups.through.objects.filter(group_id=boardAdmin.id, user_id=request.user.id).exists():
		messages.error(request, 'Cannot view settings of board not admin of')
		return redirect('/board/' + board + '/')
	boardAdminUsers = boardAdmin.user_set.all()
	boardAdminProfiles = []
	# Generate list of all board admins
	for user in boardAdminUsers:
		boardAdminProfiles.append(user.profile)
	boardGroups = boardObj.groups.all()
	userBoards = request.user.profile.boards.all()
	userGroups = request.user.groups.all()
	userGroups = userGroups.filter(name__icontains='admin')
	userAdminBoards = Board.objects.filter(groups__id__in=userGroups)

	# Initialize forms
	form = EditBoardForm()
	createAnnouncement = CreateAnnouncementForm()
	editAnnouncement = EditAnnouncementForm()

	found_entries = None
	query_string = ''
	if request.method == 'GET':
		# If name is searched, search for users by email, username, first and last name
		if('q' in request.GET) and request.GET['q'].strip():
			query_string = request.GET['q']
			entry_query = get_query(query_string, ['email', 'username', 'first_name', 'last_name',])
			found_entries = User.objects.filter(entry_query).order_by('email', 'username', 'first_name', 'last_name')

		# If send email invitation is clicked, generate token for corresponding email entered
		# Store email and token in DB, send email with signup link
		if('i' in request.GET) and request.GET['i'].strip():
			email_string = request.GET['i']
			# error if email already exists in DB with token
			if Email_Token.objects.filter(email=email_string).exists():
				messages.error(request, 'Invitation already sent to ' + email_string)
			elif User.objects.filter(email=email_string).exists(): # error if email is already used with a registered user
				messages.error(request, email_string + ' is already a registered user')
			else: 
				time = datetime.now().isoformat()
				plain = email_string + '\0' + time
				token = sha1(plain)
				new_email_token = Email_Token(email=email_string, token=token.hexdigest(), board=boardObj, expiration_date=datetime.now()+timedelta(days=3))
				signup_link = 'http://' + request.META['HTTP_HOST'] + '/' + token.hexdigest() + '/signup/'
				if SEND_EMAILS:
					send_mail('Invitation to join ' + board + '!', 'Click the following link to sign up and join ' + board + ': ' + signup_link, 'intuna@no-reply.com', [email_string], fail_silently=False,)
				new_email_token.save()

	##### PAGINATION #####
	# If no search query, display all boards in alphabetical board name order
	# if found_entries == None:
	# 	found_entries = Board.objects.all().order_by('board_name')
	# paginator = Paginator(found_entries, 20)
	# page = request.GET.get('page')
	# try:
	# 	entries = paginator.page(page)
	# except PageNotAnInteger:
	# 	entries = paginator.page(1)
	# except EmptyPage:
	# 	entries = paginator.page(paginator.num_pages)

	boardProfiles = Profile.boards.through.objects.filter(board_id=boardObj.id)
	if request.method == 'POST':
		# Edit board name
		if 'edit_board' in request.POST:
			form = EditBoardForm(request.POST)
			if form.is_valid():
				new_name = form.cleaned_data['board_name']
				boardAdmin.name = new_name + ' admin'
				boardAdmin.save(update_fields=['name'])
				boardMember.name = new_name + ' member'
				boardMember.save(update_fields=['name'])
				boardObj.board_name = new_name
				boardObj.save(update_fields=['board_name'])
		# Create announcement
		elif 'create_announcement' in request.POST:
			createAnnouncement = CreateAnnouncementForm(request.POST)
			if createAnnouncement.is_valid():
				description = createAnnouncement.cleaned_data['description']
				created_at = datetime.now()
				last_modified = datetime.now()
				date_end = createAnnouncement.cleaned_data['end_date']
				if date_end < datetime.now().date():
					messages.error(request, 'That date has already passed')
					return redirect('/settings/' + board + '/')
				user = request.user.profile
				announcement = Announcement(announcement_description=description,
											announcement_date_created=created_at,
											announcement_last_modified=last_modified,
											announcement_date_end=date_end,
											announcement_user=user,
											announcement_board=boardObj)
				announcement.save()
				return redirect('/settings/' + board + '/')
	else:
		form = EditBoardForm()
		createAnnouncement = CreateAnnouncementForm()

	boardAnnouncements = Announcement.objects.filter(announcement_board = boardObj.id)
	# if announcement end date is past current date, delete announcement	
	for announcement in boardAnnouncements:
		if announcement.announcement_date_end.date() < datetime.now().date():
		 	Announcement.objects.filter(id=announcement.id).delete()
	boardUsers = []
	for profile_board in boardProfiles:
		boardUsers.append(profile_board.profile.user)
	return render(request, 'app/board_settings.html', {'boardUsers': boardUsers, 'query_string': query_string, 'found_entries': found_entries, 'boardAnnouncements': boardAnnouncements, 'createAnnouncement': createAnnouncement, 'editAnnouncement': editAnnouncement, 'form': form, 'board' : boardObj, 'boardAdminProfiles': boardAdminProfiles, 'userAdminBoards': userAdminBoards})

# Add Member - automatically adds user to board '/add_member/<user_id>/<board>/'
# Parameters 
# - board: board name
# - user_id: unique user id in DB
@login_required
def add_member(request, user_id, board):
	boardObj = Board.objects.get(board_name=board)
 	userObj = User.objects.get(id=user_id)
	if Profile.objects.filter(pk=userObj.id, boards__pk=boardObj.id).exists():
		messages.error(request, 'Cannot add an existing member to board.')
	else:
		userObj.profile.boards.add(boardObj)
		boardMemberGroup = Group.objects.get(name=board + ' member')
		userObj.groups.add(boardMemberGroup)
	return board_settings(request, board)

# Invite User - send invited user a notification to accept board invite
# Parameters 
# - board: board name
# - user_id: unique user id in DB
# @login_required
# def invite_user(request, user_id, board):
# 	boardObj = Board.objects.get(board_name=board)
# 	userObj = User.objects.get(id=user_id)
# 	if Profile.objects.filter(pk=userObj.profile.id, boards__pk=boardObj.id).exists():
# 		messages.error(request, 'Cannot join a board you are already a member of.')
# 	else:
# 		request.user.profile.boards.add(boardObj)
# 		boardMemberGroup = Group.objects.get(name=board + ' member')
# 		request.user.groups.add(boardMemberGroup)
# 	return boards(request)

# Delete Board '/delete/<board>/'
# Parameters 
# - board: board name
@login_required
def delete_board(request, board):
	boardObj = Board.objects.get(board_name=board)
	boardAdmin = Group.objects.get(name=board + ' admin')
	if not User.groups.through.objects.filter(user_id=request.user.id, group_id=boardAdmin.id).exists():
		messages.error(request, 'Do not have permission to delete board')
		return redirect('/board/' + board + '/')
	boardGroups = boardObj.groups.all()
	for group in boardGroups:
		Group.permissions.through.objects.filter(group_id=group.id).delete()
		User.groups.through.objects.filter(group_id=group.id).delete()
		group.delete()
	Board.groups.through.objects.filter(board_id=boardObj.id).delete()
	boardObj.delete()
	return boards(request)

# Make Admin - makes an existing board member an admin '/makeadmin/<profile_id>/'
# Parameters 
# - board: board name
# - profile_id: unique profile id in DB
@login_required
def make_admin(request, profile_id, board):
	boardObj = Board.objects.get(board_name=board)
	boardAdmin = Group.objects.get(name=board + ' admin')
	boardMember = Group.objects.get(name=board + ' member')
	boardAdminUsers = boardAdmin.user_set.all()
	profile = Profile.objects.get(id=profile_id)
	currentUser = User.objects.get(id=profile.user_id)
	if currentUser in boardAdminUsers:
		messages.error(request, 'User is already an admin')
		return board_settings(request, board)
	User.groups.through.objects.filter(user_id=currentUser.id, group_id=boardMember.id).delete()
	currentUser.groups.add(boardAdmin)
	messages.success(request, currentUser.get_full_name() + ' is now an Admin')
	return board_settings(request, board)

# Remove Admin - remove existing board admin '/removeadmin/<profile_id>/'
# Parameters 
# - board: board name
# - profile_id: unique profile id in DB
@login_required
def remove_admin(request, profile_id, board):
	boardObj = Board.objects.get(board_name=board)
	boardAdmin = Group.objects.get(name=board + ' admin')
	boardMember = Group.objects.get(name=board + ' member')
	boardAdminUsers = boardAdmin.user_set.all()
	profile = Profile.objects.get(id=profile_id)
	currentUser = User.objects.get(id=profile.user_id)
	if currentUser not in boardAdminUsers:
		messages.error(request, 'User is not an admin')
		return board_settings(request, board)
	User.groups.through.objects.filter(user_id=currentUser.id, group_id=boardAdmin.id).delete()
	currentUser.groups.add(boardMember)
	messages.success(request, currentUser.get_full_name() + ' is removed from Admin')
	return board_settings(request, board)

# Edit Announcement - updates existing announcement '/editannouncement/<announceent_id>/'
# Parameters 
# - feedback_id: unique announcement id in DB
@login_required
def edit_announcement(request, announcement_id):
	announcement = Announcement.objects.get(id=announcement_id)
	board = Board.objects.get(id=announcement.announcement_board.id)
	editAnnouncement = EditAnnouncementForm()
	if request.method == 'POST':
		# Updates existing announcement
		editAnnouncement = EditAnnouncementForm(request.POST)
		if editAnnouncement.is_valid():
			description = editAnnouncement.cleaned_data['description']
			date_end = datetime.now()
			last_modified = datetime.now()
			date_end = editAnnouncement.cleaned_data['end_date']
			if date_end < datetime.now().date():
				messages.error(request, 'That date has already passed')
				return redirect('/settings/' + board.board_name + '/')
			announcement.announcement_description = description
			announcement.announcement_last_modified = last_modified
			announcement.announcement_date_end = date_end
			announcement.save(update_fields=['announcement_description', 'announcement_last_modified', 'announcement_date_end'])
		else:
			editAnnouncement = EditAnnouncementForm()
	return redirect('/settings/' + board.board_name + '/')

# Remove Announcement '/removeannouncement/<announcement_id>/'
# Parameters 
# - board: board name
# - announcement_id: unique announcement id in DB
@login_required
def remove_announcement(request, announcement_id, board):
	boardObj = Board.objects.get(board_name=board)
	boardAdmin = Group.objects.get(name=board + ' admin')
	boardMember = Group.objects.get(name=board + ' member')
	boardAdminUsers = boardAdmin.user_set.all()
	currentUser = User.objects.get(id=request.user.id)
	if currentUser not in boardAdminUsers:
		messages.error(request, 'User is not an admin')
		return board_settings(request, board)
	Announcement.objects.filter(id=announcement_id).delete()
	messages.success(request, 'Announcement deleted')
	return board_settings(request, board)