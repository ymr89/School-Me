from app.forms import EditCommentForm, EditFeedbackForm
from app.models import Board, Comment, Discussion, Feedback, Vote
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django_comments import signals
from django_comments.views.utils import next_redirect, confirmation_view

import django_comments

MAX_VOTES = 5

# Feedback - individual feedback page with comments '/<board>/members/'
# Parameters 
# - board: board name
# - feedback_id: unique feedback id in DB
@login_required
def feedback(request, board, feedback_id):
	boardObj = Board.objects.get(board_name=board)
	boardGroups = boardObj.groups.all()
	userGroups = request.user.groups.all()
	userGroups = userGroups.filter(name__icontains='admin')
	userBoards = request.user.profile.boards.all()
	userAdminBoards = Board.objects.filter(groups__id__in=userGroups)
	boardFeedbacks = Feedback.objects.filter(feedback_board=boardObj.id)
	discussionFeedback = False
	feedbackObj = get_object_or_404(Feedback, pk=feedback_id)
	# check if feedback item is discussion post
	if Discussion.objects.filter(discussion_feedback=feedbackObj.id).exists():
		discussionFeedback = True
	userFeedbacks = Feedback.objects.filter(feedback_user=request.user.profile.id)

	# Populate users who voted for the feedbacks
	upvoters = []
	downvoters = []
	upvoter_emails = []
	downvoter_emails = []
	votes = Vote.objects.all()
	for vote in votes:
		if vote.vote_feedback_id == int(feedback_id):
			# if upvote
			if vote.vote_type == 0:
				upvoters.append(vote.vote_user)
				upvoter_emails.append(vote.vote_user.user.email)
			# if downvote
			else:
				downvoters.append(vote.vote_user)
				downvoter_emails.append(vote.vote_user.user.email)

	editForm = EditFeedbackForm()
	editComment = EditCommentForm()
	if request.method == 'POST':
		# Edit and update feedback
		editForm = EditFeedbackForm(request.POST)
		if editForm.is_valid():
			title = editForm.cleaned_data['title']
			body = editForm.cleaned_data['body']
			tags = editForm.cleaned_data['tags']
			feedbackObj.feedback_title = title
			feedbackObj.feedback_description = body
			feedbackObj.feedback_last_modified = datetime.now()
			feedbackObj.save(update_fields=['feedback_title', 'feedback_description', 'feedback_last_modified'])
			return redirect('/' + board + '/feedback/' + feedback_id + '/')
		else:
			editForm = EditFeedbackForm() 

	# Check if current user upvoted/downvoted feedback item
	upvote = False
	downvote = False
	if Vote.objects.filter(vote_feedback=feedbackObj.id, vote_user=request.user.id).exists():
		vote = Vote.objects.get(vote_feedback=feedbackObj.id, vote_user=request.user.id)
		if vote.vote_type == 0:
			upvote = True
		else:
			downvote = True
	return render(request, 'comments/app/feedback.html', {'upvoters': upvoters, 'downvoters': downvoters, 'discussionFeedback': discussionFeedback, 'editCommentForm': editComment, 'upvote': upvote, 'downvote': downvote, 'board': boardObj.board_name, 'feedback': feedbackObj, 'userFeedbacks': userFeedbacks, 'editFeedbackForm': editForm, 'boardObj': boardObj, 'userAdminBoards': userAdminBoards, 'upvoter_emails': upvoter_emails, 'downvoter_emails': downvoter_emails})

# modified post_comment function taken from django_comments '/feedbacks/comments/post/'
# modified to not show preview comment page 
@login_required
def post_comment(request, next=None, using=None):
	data = request.POST.copy()
	if request.user.is_authenticated():
		if not data.get('name', ''):
			data["name"] = request.user.get_full_name() or request.user.get_username()
		if not data.get('email', ''):
			data["email"] = request.user.email

    # Look up the object we're trying to comment about
	ctype = data.get("content_type")
	object_pk = data.get("object_pk")
	if ctype is None or object_pk is None:
	    return CommentPostBadRequest("Missing content_type or object_pk field.")
	try:
	    model = apps.get_model(*ctype.split(".", 1))
	    target = model._default_manager.using(using).get(pk=object_pk)
	except TypeError:
	    return CommentPostBadRequest(
	        "Invalid content_type value: %r" % escape(ctype))
	except AttributeError:
	    return CommentPostBadRequest(
	        "The given content-type %r does not resolve to a valid model." % escape(ctype))
	except ObjectDoesNotExist:
	    return CommentPostBadRequest(
	        "No object matching content-type %r and object PK %r exists." % (
	            escape(ctype), escape(object_pk)))
	except (ValueError, ValidationError) as e:
	    return CommentPostBadRequest(
	        "Attempting go get content-type %r and object PK %r exists raised %s" % (
	            escape(ctype), escape(object_pk), e.__class__.__name__))

	# Do we want to preview the comment?
	preview = "preview" in data

	# Construct the comment form
	form = django_comments.get_form()(target, data=data)

	# Check security information
	if form.security_errors():
	    return CommentPostBadRequest(
	        "The comment form failed security verification: %s" % escape(str(form.security_errors())))

	# If there are errors or if we requested a preview show the comment
	if form.errors or preview:
		messages.error(request, "Cannot submit a blank comment form")
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	# Otherwise create the comment
	comment = form.get_comment_object()
	comment.ip_address = request.META.get("REMOTE_ADDR", None)
	if request.user.is_authenticated():
	    comment.user = request.user

	# Signal that the comment is about to be saved
	responses = signals.comment_will_be_posted.send(
	    sender=comment.__class__,
	    comment=comment,
	    request=request
	)

	for (receiver, response) in responses:
	    if response is False:
	        return CommentPostBadRequest(
	            "comment_will_be_posted receiver %r killed the comment" % receiver.__name__)

	# Save the comment and signal that it was saved
	comment.save()
	signals.comment_was_posted.send(
	    sender=comment.__class__,
	    comment=comment,
	    request=request
	)

	return next_redirect(request, fallback=next or 'comments-comment-done',
	                     c=comment._get_pk_val())

# Edit Comment - updates comment in DB '/editcomment/<comment_id>/'
# Parameters 
# - comment_id: unique comment id in DB
# - board: board name
# - feedback_id: unique feedback id in DB
@login_required
def edit_comment(request, comment_id, board, feedback_id):
	print "in edit comment function"
	boardObj = Board.objects.get(board_name=board)
	feedbackObj = get_object_or_404(Feedback, pk=feedback_id)
	commentObj = get_object_or_404(Comment, pk=comment_id)
	form = EditCommentForm()
	if request.method == 'POST':
		# update existing comment
		form = EditCommentForm(request.POST)
		if form.is_valid():
			comment = form.cleaned_data['comment']
			commentObj.comment = comment
			commentObj.submit_date = datetime.now()
			commentObj.save(update_fields=['comment', 'submit_date'])
			return redirect('/' + board + '/feedback/' + str(feedbackObj.id) + '/')
		else:
			form = EditCommentForm()

	return feedback(request, board, feedback_id)

# Delete Comment '/deletecomment/<comment_id>/'
# Parameters 
# - comment_id: unique comment id in DB
@login_required
def delete_comment(request, comment_id):
	delete_comment_by_id(comment_id);
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# recursively goes through the tree of existing comments and deletes the comment's children and itself
def delete_comment_by_id(comment):
	if Comment.objects.filter(object_pk=comment).exists():
		tempComments = Comment.objects.filter(object_pk=comment)
		for comments in tempComments:
			delete_comment_by_id(comments.id)
			comments.delete()
	if Comment.objects.filter(id=comment).exists():
		Comment.objects.get(id=comment).delete()
	return

# Delete Feedback - deletes feedback from board page '/deletefeedback/<feedback_id>/'
# Parameters 
# - board: board name
# - feedback_id: unique feedback id in DB
@login_required
def delete_feedback(request, feedback_id, board):
	Feedback.objects.get(id=feedback_id).delete()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# Delete Feedback - deletes feedback from individual feedback page '/deletefeedback_fromfeedback/<feedback_id>/'
# Parameters 
# - board: board name
# - feedback_id: unique feedback id in DB
@login_required
def delete_feedback_from_feedback(request, feedback_id, board):
	print feedback_id
	feedbackItem = Feedback.objects.get(id=feedback_id)
	redirectLink = ''
	discussion = False
	if Discussion.objects.filter(discussion_feedback=feedback_id).exists():
		discussion = True
	feedbackItem.delete()
	if discussion:
		return redirect('/' + board + '/discussion/')
	else:
		return redirect('/board/' + board + '/')

# Edit Feedback - updates existing feedback '/editfeedback/<feedback_id>/'
# Parameters 
# - board: board name
# - feedback_id: unique feedback id in DB
@login_required
def edit_feedback(request, feedback_id, board):
	boardObj = Board.objects.get(board_name=board)
	boardGroups = boardObj.groups.all()
	userGroups = request.user.groups.all()
	userBoardAccess = False
	boardFeedbacks = Feedback.objects.filter(feedback_board=boardObj.id)
	userFeedbacks = Feedback.objects.filter(feedback_user=request.user.profile.id)
	
	# Check if user is a member of the board
	for group in boardGroups:
		if group in userGroups:
			userBoardAccess = True
			break
	# If user is not a member of any of the board's groups, deny access
	if not userBoardAccess:
		messages.error(request, 'Cannot view a board you are not a member of.')
		return boards(request)

	post = Feedback.objects.get(id=feedback_id)
	form = EditFeedbackForm()
	if post.feedback_user == request.user.profile:
		if request.method == 'POST':
			# updates existing feedback
			form = EditFeedbackForm(request.POST)
			if form.is_valid():
				title = form.cleaned_data['title']
				body = form.cleaned_data['body']
				tags = form.cleaned_data['tags']
				post.feedback_title = title
				post.feedback_description = body
				post.feedback_last_modified = datetime.now()
				post.save(update_fields=['feedback_title', 'feedback_description', 'feedback_last_modified'])
				print "saved feedback " + str(post.id)
				return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
		else:
			form = EditFeedbackForm()
	else:
		messages.error(request, 'Cannot edit a post you did not write.')
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# Update Upvote - updates feedback if upvoted and updates user's vote count '/upvote/<feedback_id>/<board>/'
# Parameters 
# - board: board name
# - feedback_id: unique feedback id in DB
@login_required
def update_upvote(request, feedback_id, board):
	feedback = Feedback.objects.get(id=feedback_id)
	totalVotes = Vote.objects.filter(vote_user=request.user.id)
	if len(totalVotes) >= MAX_VOTES:
		messages.error(request, 'Already reached max number of votes.')
		return redirect('/board/' + board + '/')
	# If user already cast a vote on this feedback
	if Vote.objects.filter(vote_feedback=feedback_id, vote_user=request.user.id).exists():
		vote = Vote.objects.get(vote_feedback=feedback_id, vote_user=request.user.id)
		# if downvote changed to upvote
		if vote.vote_type == 1:
			vote.vote_type = 0
			vote.save(update_fields=['vote_type'])
			feedback.feedback_upvotes = feedback.feedback_upvotes + 1
			feedback.feedback_downvotes = feedback.feedback_downvotes - 1
			feedback.save(update_fields=['feedback_upvotes', 'feedback_downvotes'])
		else: # if same arrow clicked, cancel vote
			vote.delete()
			feedback.feedback_upvotes = feedback.feedback_upvotes - 1
			feedback.save(update_fields=['feedback_upvotes'])
	else: # Else create new vote
		vote = Vote(vote_user=request.user.profile, vote_feedback=feedback, vote_type=0)
		vote.save()
		feedback.feedback_upvotes = feedback.feedback_upvotes + 1
		feedback.save(update_fields=['feedback_upvotes'])
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# Update Downvote - updates feedback if downvoted and updates user's vote count '/downvote/<feedback_id>/<board>/'
# Parameters 
# - board: board name
# - feedback_id: unique feedback id in DB
@login_required
def update_downvote(request, feedback_id, board):
	feedback = Feedback.objects.get(id=feedback_id)
	totalVotes = Vote.objects.filter(vote_user=request.user.id)
	if len(totalVotes) >= MAX_VOTES:
		messages.error(request, 'Already reached max number of votes.')
		return redirect('/board/' + board + '/')
	# If user already cast a vote on this feedback
	if Vote.objects.filter(vote_feedback=feedback_id, vote_user=request.user.id).exists():
		vote = Vote.objects.get(vote_feedback=feedback_id, vote_user=request.user.id)
		# if upvote changed to downvote
		if vote.vote_type == 0:
			vote.vote_type = 1
			vote.save(update_fields=['vote_type'])
			feedback.feedback_upvotes = feedback.feedback_upvotes - 1
			feedback.feedback_downvotes = feedback.feedback_downvotes + 1
			feedback.save(update_fields=['feedback_upvotes', 'feedback_downvotes'])
		else: # if same arrow clicked, cancel vote
			vote.delete()
			feedback.feedback_downvotes = feedback.feedback_downvotes - 1
			feedback.save(update_fields=['feedback_downvotes'])
	else: # Else create new vote
		vote = Vote(vote_user=request.user.profile, vote_feedback=feedback, vote_type=1)
		vote.save()
		feedback.feedback_downvotes = feedback.feedback_downvotes + 1
		feedback.save(update_fields=['feedback_downvotes'])
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
