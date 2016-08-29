from app.forms import CreateBoardForm, EditProfileForm
from app.models import Announcement, Board, Feedback, Organization, Profile, Vote
from app.views.search import get_query
from app.views.add_permissions import addAdminPermissions, addMemberPermissions
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group, Permission
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render, redirect
from itertools import chain

import lifter

# User home page - displays all feedback from boards the user is a member of '/userhome/'
@login_required
def userhome(request):
	userBoards = request.user.profile.boards.all()
	userBoardsFeedback = []
	userBoardsAnnouncement = []
	# Populate feed with feedback from all boards the user is a member of
	for board in userBoards:
		boardFeedback = Feedback.objects.filter(feedback_board=board.id)
		boardAnnouncement = Announcement.objects.filter(announcement_board=board.id)
		userBoardsFeedback = list(chain(userBoardsFeedback, boardFeedback))
		userBoardsAnnouncement = list(chain(userBoardsAnnouncement, boardAnnouncement))
	# Order feedbacks so that most recent is at the top
	FeedbackModel = lifter.models.Model('Feedback')
	manager = FeedbackModel.load(userBoardsFeedback)
	userBoardsFeedback = manager.order_by('-feedback_date_created')
	# Get all current user's feedbacks and populate upvotes/downvotes for each feedback they voted for
	userFeedbacks = Feedback.objects.filter(feedback_user=request.user.profile.id)
	upvotes = []
	downvotes = []
	for feedback in userBoardsFeedback:
		if Vote.objects.filter(vote_feedback=feedback.id, vote_user=request.user.id).exists():
			vote = Vote.objects.get(vote_feedback=feedback.id, vote_user=request.user.id)
			if vote.vote_type == 0:
				upvotes.append(True)
				downvotes.append(False)
			else:
				upvotes.append(False)
				downvotes.append(True)
		else:
			upvotes.append(False)
			downvotes.append(False)
	return render(request, 'app/userhome.html', {'userBoardsAnnouncement': userBoardsAnnouncement, 'upvotes': upvotes, 'downvotes': downvotes, 'userBoardsFeedback': userBoardsFeedback, 'userFeedbacks': userFeedbacks})

# Profile - find profile to display for the profile page '/profile/<profile_id>/'
# Parameters 
# - profile_id: unique profile id in DB
@login_required
def profile(request, profile_id):
	profileObj = get_object_or_404(Profile, pk=profile_id)
	return render(request, 'app/profile.html', {'profile': profileObj})

# Edit - edit profile '/profile/<profile_id>/edit/'
# Parameters 
# - profile_id: unique profile id in DB
@login_required
def edit(request, profile_id):
	profileObj = get_object_or_404(Profile, pk=profile_id)
	if request.user.profile.id != int(profile_id):
		messages.error(request, 'Cannot edit a profile that is not yours.')
		return redirect('/profile/' + profile_id + '/')
	user = get_object_or_404(User, pk=profile_id)
	# get users current organization
	CurrentOrg = get_object_or_404(Organization, pk=profileObj.user_organization.id)
	# get list of all organizations
	Orgs = Organization.objects.all()
	# assume organization does not already exist
	orgExists = 0
	form = EditProfileForm()
	if request.method == 'POST':
		form = EditProfileForm(request.POST)
		if form.is_valid():
			NewOrgName = form.cleaned_data['organization']
			NewEmail = form.cleaned_data['email']
			NewFirst = form.cleaned_data['first']
			NewLast = form.cleaned_data['last']
			# if organization name is same as any existing organization
			for org in Orgs:
				if NewOrgName == org.organization_name:
					orgExists = 1
					CurrentOrg.organization_name = org.organization_name
					CurrentOrg.id = org.id
					CurrentOrg.save()
					profileObj.user_organization = CurrentOrg
					profileObj.save(update_fields=['user_organization'])
			# if no matches found, create new organization
			if orgExists == 0:
				new_org = Organization(organization_name=NewOrgName)
				new_org.save()
				profileObj.user_organization = new_org
				profileObj.save(update_fields=['user_organization'])			
			if NewEmail != '':
				user.email = NewEmail
				user.save(update_fields=['email'])
			if NewFirst != '':
				user.first_name = NewFirst
				user.save(update_fields=['first_name'])
			if NewLast != '':
				user.last_name = NewLast
				user.save(update_fields=['last_name'])
			messages.success(request, 'Profile successfully saved')
		else:
			form = EditProfileForm()
	return render(request, 'app/edit.html', {'profile': profileObj, 'form': form})

# Notifications '/notifications/'
@login_required
def notifications(request):
	return render(request, 'app/notifications.html')

# Boards - your boards listing '/boards/'
@login_required
def boards(request):
	boards = request.user.profile.boards.all()
	userBoards = request.user.profile.boards.all()
	userGroups = request.user.groups.all()
	userGroups = userGroups.filter(name__icontains='admin')
	userAdminBoards = Board.objects.filter(groups__id__in=userGroups)
	form = CreateBoardForm()
	if request.method == 'POST':
		form = CreateBoardForm(request.POST)
		if form.is_valid():
			board_name = form.cleaned_data['board_name']
			board_privacy = form.cleaned_data['board_privacy']
			board = Board(board_name=board_name)
			newAdminGroup = Group(name=board_name + ' admin')
			newAdminGroup.save()
			addAdminPermissions(newAdminGroup)
			newMemberGroup = Group(name=board_name + ' member')
			newMemberGroup.save()
			addMemberPermissions(newMemberGroup)
			if board_privacy == '0':
				board.board_private = False
			elif board_privacy == '1':
				board.board_private = True
			board.save()
			board.groups.add(newAdminGroup)
			board.groups.add(newMemberGroup)
			request.user.profile.boards.add(board)
			request.user.groups.add(newAdminGroup)
			return redirect('/boards/')
	else:
		form = CreateBoardForm()
	return render(request, 'app/your_boards.html', {'userAdminBoards': userAdminBoards, 'userBoards': userBoards, 'boards': boards, 'form': form})

# Join board - lists all public boards '/join_board/'
@login_required
def join_board(request):
	# Queries and finds boards that match query_string
	found_entries = None
	query_string = ''
	if request.method == 'GET':
		if('q' in request.GET) and request.GET['q'].strip():
			query_string = request.GET['q']
			entry_query = get_query(query_string, ['board_name',])
			found_entries = Board.objects.filter(entry_query).order_by('board_name')
	# If no search query, display all boards in alphabetical board name order
	if found_entries == None:
		found_entries = Board.objects.all().order_by('board_name')
	# Display 20 found_entries per page
	paginator = Paginator(found_entries, 20)
	page = request.GET.get('page')
	try:
		entries = paginator.page(page)
	except PageNotAnInteger:
		entries = paginator.page(1)
	except EmptyPage:
		entries = paginator.page(paginator.num_pages)
	boards = request.user.profile.boards.all()
	userBoards = request.user.profile.boards.all()
	userGroups = request.user.groups.all()
	userGroups = userGroups.filter(name__icontains='admin')
	userAdminBoards = Board.objects.filter(groups__id__in=userGroups)
	return render(request, 'app/join_board.html', {'query_string': query_string, 'userAdminBoards': userAdminBoards, 'userBoards': userBoards, 'boards': boards, 'found_entries': entries})

# Join Board '/join/<board>/'
# Parameters 
# - board: board name
@login_required
def join(request, board):
	boardObj = Board.objects.get(board_name=board)
	if Profile.objects.filter(pk=request.user.profile.id, boards__pk=boardObj.id).exists():
		messages.error(request, 'Cannot join a board you are already a member of.')
	else:
		request.user.profile.boards.add(boardObj)
		boardMemberGroup = Group.objects.get(name=board + ' member')
		request.user.groups.add(boardMemberGroup)
	return boards(request)

# Create board '/create_board/'
@login_required
def create_board(request):
	form = CreateBoardForm()
	if request.method == 'POST':
		form = CreateBoardForm(request.POST)
		if form.is_valid():
			board_name = form.cleaned_data['board_name']
			board_privacy = form.cleaned_data['board_privacy']
			board = Board(board_name=board_name)
			newAdminGroup = Group(name=board_name + ' admin')
			newAdminGroup.save()
			addAdminPermissions(newAdminGroup)
			newMemberGroup = Group(name=board_name + ' member')
			newMemberGroup.save()
			addMemberPermissions(newMemberGroup)
			if board_privacy == '0': # if not a private board
				board.board_private = False
			elif board_privacy == '1': # else if private board
				board.board_private = True
			board.save()
			board.groups.add(newAdminGroup)
			board.groups.add(newMemberGroup)
			request.user.profile.boards.add(board)
			request.user.groups.add(newAdminGroup)
			return redirect('/boards/')
	else:
		form = CreateBoardForm()
	return render(request, 'app/create_board.html', {'form': form})