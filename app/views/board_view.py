from app.forms import DiscussionForm, EditDiscussionForm, EditFeedbackForm, FilterDiscussionForm, FilterForm, FeedbackForm, UploadFileForm
from app.models import Announcement, Board, Bug, Discussion, Feature_Request, Feedback, File, Status, Vote
from app.views.search import get_query
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from itertools import chain
from rest_framework.reverse import reverse

import lifter

# used for file related functions
from wsgiref.util import FileWrapper
import cStringIO as StringIO
import os, mimetypes, urllib

#Setting this flag true sends emails out
SEND_EMAILS = True

# Board - each individual board's feedback page '/board/<board>/'
# Parameters 
# - board: board name
@login_required
def board(request, board):
	boardObj = Board.objects.get(board_name=board)
	boardGroups = boardObj.groups.all()
	userGroups = request.user.groups.all()
	userBoardAccess = False
	boardBugs = Bug.objects.filter(bug_feedback__feedback_board=boardObj.id)
	boardFeatureRequests = Feature_Request.objects.filter(feature_request_feedback__feedback_board=boardObj.id)
	boardFeedbackBugs = Feedback.objects.filter(id__in=boardBugs.values('bug_feedback'))
	boardFeedbackFeatureRequests = Feedback.objects.filter(id__in=boardFeatureRequests.values('feature_request_feedback'))
	boardFeedbacks = list(chain(boardFeedbackBugs, boardFeedbackFeatureRequests))
	boardAdminGroup = boardGroups.filter(name__icontains='admin')
	boardAdminGroup = boardAdminGroup[0]
	boardAdmins = User.objects.filter(groups__id=boardAdminGroup.id)
	userFeedbacks = Feedback.objects.filter(feedback_user=request.user.profile.id)
	boardAnnouncements = Announcement.objects.filter(announcement_board=boardObj.id)

	# Check if user is a member of the board
	for group in boardGroups:
		if group in userGroups:
			userBoardAccess = True
			break

	# If user is not a member of any of the board's groups, deny access
	if not userBoardAccess:
		messages.error(request, 'Cannot view a board you are not a member of.')
		return boards(request)

	# Initialize forms
	form = FeedbackForm()
	filterFeedback = FilterForm()
	editFeedback = EditFeedbackForm()

	posts = boardObj.feedback_set.all()

	# Initialize search variables
	found_entries = None
	query_string = ''

	# Post requests
	if request.method == 'POST':
		# New feedback post
		if 'post_feedback' in request.POST:
			form = FeedbackForm(request.POST)
			#needed when file upload gets implemented
			#form = FeedbackForm(request.POST, request.FILES)
			if form.is_valid():
				print request.FILES
				title = form.cleaned_data['title']
				body = form.cleaned_data['body']
				tags = form.cleaned_data['tags']
				feedbackType = form.cleaned_data['feedbackType']
				created_at = datetime.now()
				last_modified = datetime.now()
				user = request.user.profile
				status = Status(status_name="Unresolved", status_board=boardObj)
				status.save()
				new_feedback = Feedback(feedback_title=title,
										feedback_description=body,
										feedback_date_created=created_at,
										feedback_last_modified=last_modified,
										#feedback_file=request.FILES['post_feedback'],
										feedback_user=user,
										feedback_board=boardObj,
										feedback_status=status,
										feedback_upvotes=0,
										feedback_downvotes=0)
				new_feedback.save()				
				if feedbackType == '0': # feature request
					new_feature_request = Feature_Request(feature_request_feedback=new_feedback, feature_request_status=status)
					new_feature_request.save()
				elif feedbackType == '1': # bug report
					new_bug_report = Bug(bug_feedback=new_feedback, bug_status=status)
					new_bug_report.save()
				feedback_link = reverse('feedback', kwargs={'board':board, 'feedback_id': new_feedback.id})
				feedback_link = 'http://' + request.META['HTTP_HOST'] + feedback_link[4:]
				body = 'View feedback post at: ' + body + '\n\n' + feedback_link
				# Send email to all board admins when new post is created if SEND_EMAILS = True
				if SEND_EMAILS:
					for admin in boardAdmins:
						send_mail('New Post From ' + boardObj.board_name + ': ' + title, body, 'intuna@no-reply.com', [admin.email], fail_silently=False,)
				return redirect('/board/' + board + '/')
		else: 
			# Search for feedback
			if('q' in request.POST) and request.POST['q'].strip():
				print 'QUERY FOUND'
				query_string = request.POST['q']
				# Search all feedback titles and feedback descriptions
				entry_query = get_query(query_string, ['feedback_title','feedback_description'])
				# Order by feedback title
				found_entries = Feedback.objects.filter(entry_query).order_by('feedback_title')
				board_entries = []
				# Filter for posts only in this board
				for entry in found_entries:
					if entry in boardFeedbacks:
						board_entries.append(entry)
				boardFeedbacks = board_entries

			# Filter posts
			filterFeedback = FilterForm(request.POST)
			if filterFeedback.is_valid():
				filterType = filterFeedback.cleaned_data['filterType']
				postType = filterFeedback.cleaned_data['postType']
				if postType == '1': # feature request
					featureRequests = Feature_Request.objects.all()
					newBoardFeedbacks = []
					for featureReq in featureRequests:
						if featureReq.feature_request_feedback.feedback_board.id == boardObj.id and featureReq.feature_request_feedback in boardFeedbacks:
							newBoardFeedbacks.append(featureReq.feature_request_feedback)
					boardFeedbacks = newBoardFeedbacks
				elif postType == '2': #bug report
					bugReports = Bug.objects.all()
					newBoardFeedbacks = []
					for bugRep in bugReports:
						if bugRep.bug_feedback.feedback_board.id == boardObj.id and bugRep.bug_feedback in boardFeedbacks:
							newBoardFeedbacks.append(bugRep.bug_feedback)
					boardFeedbacks = newBoardFeedbacks
				FeedbackModel = lifter.models.Model('Feedback')
				manager = FeedbackModel.load(boardFeedbacks)
				if filterType == '0': # sort by most recent as the top
					boardFeedbacks = manager.order_by('-feedback_date_created')
				elif filterType == '1': # sort by most popular posts at the top
					boardFeedbacks = manager.order_by('-feedback_upvotes', 'feedback_downvotes')
				elif filterType == '2': # sort by oldest posts at the top
					boardFeedbacks = manager.order_by('feedback_date_created')
	else:
		form = FeedbackForm()
		filterFeedback = FilterForm()

	userBoards = request.user.profile.boards.all()
	userGroups = request.user.groups.all()
	userGroups = userGroups.filter(name__icontains='admin')
	userAdminBoards = Board.objects.filter(groups__id__in=userGroups)

	# Populate user upvotes/downvotes for board feedbacks
	upvotes = []
	downvotes = []
	for feedback in boardFeedbacks:
		if Vote.objects.filter(vote_feedback=feedback.id, vote_user=request.user.id).exists():
			vote = Vote.objects.get(vote_feedback=feedback.id, vote_user=request.user.id)
			if vote.vote_type == 0: # if upvote
				upvotes.append(True)
				downvotes.append(False)
			else: # if downvote
				upvotes.append(False)
				downvotes.append(True)
		else:
			upvotes.append(False)
			downvotes.append(False)
	return render(request, 'app/board.html', {'query_string': query_string, 'boardAnnouncements': boardAnnouncements, 'filterform': filterFeedback, 'editFeedback': editFeedback, 'upvotes': upvotes, 'downvotes': downvotes, 'form': form, 'board': boardObj.board_name, 'boardid': boardObj.id, 'boardObj': boardObj, 'userAdminBoards': userAdminBoards, 'feedbacks': boardFeedbacks, 'userFeedbacks': userFeedbacks})

# Discussion - each individual board's discussion page '/<board>/discussion/'
# Parameters 
# - board: board name
@login_required
def discussion(request, board):
	boardObj = Board.objects.get(board_name=board)
	boardGroups = boardObj.groups.all()
	userGroups = request.user.groups.all()
	boardAdminGroup = boardGroups.filter(name__icontains='admin')
	boardAdminGroup = boardAdminGroup[0]
	boardAdmins = User.objects.filter(groups__id=boardAdminGroup.id)
	userBoardAccess = False

	# Check if user is a member of the board
	for group in boardGroups:
		if group in userGroups:
			userBoardAccess = True
			break
	
	# If user is not a member of any of the board's groups, deny access
	if not userBoardAccess:
		messages.error(request, 'Cannot view a board you are not a member of.')
		return boards(request)
	
	form = DiscussionForm()
	editPost = EditDiscussionForm()
	boardDiscussions = Discussion.objects.filter(discussion_feedback__feedback_board=boardObj.id)
	boardFeedbackDiscussions = Feedback.objects.filter(id__in=boardDiscussions.values('discussion_feedback'))
	userFeedbacks = Feedback.objects.filter(feedback_user=request.user.profile.id)
	filterFeedback = FilterDiscussionForm()
	found_entries = None
	query_string = ''
	if request.method == 'POST':
		# Creates new discussion post
		if 'post_feedback' in request.POST:
			form = DiscussionForm(request.POST)
			if form.is_valid():
				title = form.cleaned_data['title']
				body = form.cleaned_data['body']
				tags = form.cleaned_data['tags']
				created_at = datetime.now()
				last_modified = datetime.now()
				user = request.user.profile
				status = Status(status_name="Unresolved", status_board=boardObj)
				status.save()
				new_feedback = Feedback(feedback_title=title,
										feedback_description=body,
										feedback_date_created=created_at,
										feedback_last_modified=last_modified,
										feedback_user=user,
										feedback_board=boardObj,
										feedback_status=status,
										feedback_upvotes=0,
										feedback_downvotes=0)
				new_feedback.save()
				new_discussion_post = Discussion(discussion_feedback=new_feedback, discussion_status=status)
				new_discussion_post.save()
				# Send email to all board admins when new post is created if SEND_EMAILS = True
				feedback_link = reverse('feedback', kwargs={'board':board, 'feedback_id': new_feedback.id})
				feedback_link = 'http://' + request.META['HTTP_HOST'] + feedback_link[4:]
				body = 'View discussion post at: ' + body + '\n\n' + feedback_link
				if SEND_EMAILS:
					for admin in boardAdmins:
						send_mail('New Post From ' + boardObj.board_name + ': ' + title, body, 'intuna@no-reply.com', [admin.email], fail_silently=False,)
				return redirect('/' + boardObj.board_name + '/discussion/')
		else:
			# Filter discussion posts; includes search query
			filterFeedback = FilterDiscussionForm(request.POST)
			if('q' in request.POST) and request.POST['q'].strip():
				print 'QUERY FOUND'
				query_string = request.POST['q']
				entry_query = get_query(query_string, ['feedback_title','feedback_description'])
				found_entries = Feedback.objects.filter(entry_query).order_by('feedback_title')
				board_entries = []
				for entry in found_entries:
					if entry in boardFeedbackDiscussions:
						board_entries.append(entry)
				boardFeedbackDiscussions = board_entries
			if filterFeedback.is_valid():
				filterType = filterFeedback.cleaned_data['filterType']
				FeedbackModel = lifter.models.Model('Feedback')
				manager = FeedbackModel.load(boardFeedbackDiscussions)
				if filterType == '0': # sort by most recent as the top
					boardFeedbackDiscussions = manager.order_by('-feedback_date_created')
				elif filterType == '1': # sort by most popular posts at the top
					boardFeedbackDiscussions = manager.order_by('-feedback_upvotes', 'feedback_downvotes')
				elif filterType == '2': # sort by oldest as the top
					boardFeedbackDiscussions = manager.order_by('feedback_date_created')
	else:
		form = DiscussionForm()
		filterFeedback = FilterDiscussionForm()

	userBoards = request.user.profile.boards.all()
	userGroups = request.user.groups.all()
	userGroups = userGroups.filter(name__icontains='admin')
	userAdminBoards = Board.objects.filter(groups__id__in=userGroups)

	# Populate user upvotes/downvotes for board feedbacks
	upvotes = []
	downvotes = []
	for feedback in boardFeedbackDiscussions:
		if Vote.objects.filter(vote_feedback=feedback.id, vote_user=request.user.id).exists():
			vote = Vote.objects.get(vote_feedback=feedback.id, vote_user=request.user.id)
			if vote.vote_type == 0: # if upvote
				upvotes.append(True)
				downvotes.append(False)
			else: # if downvote
				upvotes.append(False)
				downvotes.append(True)
		else:
			upvotes.append(False)
			downvotes.append(False)
	return render(request, 'app/discussion.html', {'query_string': query_string, 'filterform': filterFeedback, 'userFeedbacks': userFeedbacks, 'upvotes': upvotes, 'downvotes': downvotes, 'posts': boardFeedbackDiscussions, 'editDiscussion': editPost, 'form': form, 'board': boardObj.board_name, 'boardid': boardObj.id, 'boardObj': boardObj, 'userAdminBoards': userAdminBoards})

# Members - board members list '/<board>/members/'
# Parameters
# - board: board name
@login_required
def members(request, board):
	boardObj = Board.objects.get(board_name=board)
	boardGroups = boardObj.groups.all()
	userGroups = request.user.groups.all()
	boardAdmin = Group.objects.get(name=board + ' admin')
	boardMember = Group.objects.get(name=board + ' member')
	boardAdminUsers = boardAdmin.user_set.all()
	userBoards = request.user.profile.boards.all()
	userGroups = userGroups.filter(name__icontains='admin')
	userAdminBoards = Board.objects.filter(groups__id__in=userGroups)
	return render(request, 'app/members.html', {'board': boardObj.board_name, 'boardid': boardObj.id, 'boardObj': boardObj, 'userAdminBoards': userAdminBoards})

# Files - upload files to boards '/<board>/files/'
# Parameters
# - board: board name
@login_required
def files(request, board):
	boardObj = Board.objects.get(board_name=board)
	boardGroups = boardObj.groups.all()
	userGroups = request.user.groups.all()
	boardAdmin = Group.objects.get(name=board + ' admin')
	boardMember = Group.objects.get(name=board + ' member')
	boardAdminUsers = boardAdmin.user_set.all()
	userBoards = request.user.profile.boards.all()
	userGroups = userGroups.filter(name__icontains='admin')
	userAdminBoards = Board.objects.filter(groups__id__in=userGroups)
	if request.method == 'POST':
		# Uploads file
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			name = form.cleaned_data['name']
			description = form.cleaned_data['description']
			date_uploaded = timezone.now()
			user = user = request.user.profile
			newfile = File(file_date_uploaded=date_uploaded,
							file_name=name,
							file_description=description,
							file_file = request.FILES['file_file'],
							file_board=boardObj,
							file_user=user)
			if not request.user.groups.through.objects.filter(group_id=boardAdmin.id, user_id=request.user.id).exists():
				messages.error(request, 'Cannot upload a file to a board you are not an admin of')
				return redirect('/' + boardObj.board_name + '/files/')
			newfile.save()
			return redirect('/' + boardObj.board_name + '/files/')
	else:
		form = UploadFileForm()
	files = File.objects.all()
	print files
	return render(request, 'app/files.html', {'form': form, 'board' : boardObj.board_name, 'boardObj': boardObj, 'files': files, 'boardid': boardObj.id, 'userAdminBoards': userAdminBoards})

@login_required
def delete_file(request, file_id):
	File.objects.get(id=file_id).delete()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def download_file(request, file_id):
	fileObj = get_object_or_404(File, pk=file_id)
	# remove ./ from beginning of file_file to get filename
	filename = str(fileObj.file_file)
	filename = filename[2:]
	path = os.path.expanduser('~/files/')
	wrapper = FileWrapper(file(filename,'rb'))
	response = HttpResponse(wrapper, content_type=mimetypes.guess_type(filename)[0])
	response['Content-Length'] = os.path.getsize(filename)
	response['Content-Disposition'] = "attachment; filename=" + filename
	return response

# Leave Board '/leave/<board>/'
# Parameters 
# - board: board name
@login_required
def leave_board(request, board):
	boardObj = Board.objects.get(board_name=board)
	boardGroups = boardObj.groups.all()
	boardAdmin = Group.objects.get(name=board + ' admin')
	if (boardAdmin.user_set.all().count() <= 1) and request.user.groups.through.objects.filter(group_id=boardAdmin.id, user_id=request.user.id).exists():
		messages.error(request, 'Cannot leave as last board admin, please delete the board to leave.')
		return redirect('/board/' + board + '/')
	Profile.boards.through.objects.filter(board_id=boardObj.id, profile_id=request.user.profile.id).delete()
	for group in boardGroups:
		if User.groups.through.objects.filter(user_id=request.user.id, group_id=group.id).exists():
			group.user_set.remove(request.user)
	return boards(request)
