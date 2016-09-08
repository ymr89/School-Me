import datetime

from django.db import models
from django.core.urlresolvers import reverse
from django.core.files import File
from django.utils import timezone
from django.contrib.auth.models import User, Group, Permission
from django_comments.models import Comment

class Organization(models.Model):
	id = models.AutoField(primary_key=True)
	organization_name = models.CharField(max_length=30)

	def __str__(self):
		return "%s" % self.organization_name

class Board(models.Model):
	id = models.AutoField(primary_key=True)
	board_name = models.CharField(max_length = 30)
	groups = models.ManyToManyField(Group) # Each board has a number of groups with different permissions
	board_private = models.BooleanField(default=False)

	def __str__(self):
		return "%s" % self.board_name

# invites field was made to keep track of all boards a user is invited to if a user had to accept a board invitation before being added to it
# invite notification would show up in the notifications page
# currently, users are automatically added to boards when an admin invites them
class Profile(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	user_organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
	boards = models.ManyToManyField(Board, blank=True, related_name='profile_boards')
	invites = models.ManyToManyField(Board, blank=True, related_name='profile_invites')

	def __str__(self):
		return "%s" % self.user

##### UNIMPLEMENTED ##### - the status model might need to be rethought...USED in feedback, discussion, feature request, and bug
# board admins should be able to make any number of statuses they want for their board
class Status(models.Model):
	id = models.AutoField(primary_key=True)
	status_name = models.CharField(max_length = 30)
	status_board = models.ForeignKey(Board, on_delete=models.CASCADE)

	def __str__(self):
		return "%s" % self.status_name

# Stores the token used for email invitation 
class Email_Token(models.Model):
	id = models.AutoField(primary_key=True)
	email = models.EmailField()
	token = models.CharField(max_length = 50)
	board = models.ForeignKey(Board, on_delete=models.CASCADE)
	expiration_date = models.DateTimeField('token expiration date')

class Feedback(models.Model):
	id = models.AutoField(primary_key=True)
	feedback_title = models.CharField(max_length = 50)
	feedback_description = models.TextField()
	feedback_date_created = models.DateTimeField('date feedback created')
	feedback_last_modified = models.DateTimeField('date feedback last modified')
	#set blank=True to make file field optional, allows for blank entry in database
	#feedback file upload is not yet implemented, but the field is here
	feedback_file = models.FileField(blank=True)
	feedback_user = models.ForeignKey(Profile, on_delete=models.CASCADE)
	feedback_board = models.ForeignKey(Board, on_delete=models.CASCADE)
	feedback_status = models.ForeignKey(Status, on_delete=models.CASCADE) 
	feedback_upvotes = models.IntegerField(default=0)
	feedback_downvotes = models.IntegerField(default=0)

	class Meta:
		verbose_name = "feedback"
		verbose_name_plural = "feedbacks"

	def __unicode__(self):
		return self.feedback_title

	def __str__(self):
		return "%s" % self.feedback_title

	def get_queryset(self):
		return Feedback.objects.all()

class Announcement(models.Model):
	id = models.AutoField(primary_key=True)
	announcement_description = models.TextField()
	announcement_date_created = models.DateTimeField('date announcement created')
	announcement_last_modified = models.DateTimeField('date announcement last modified')
	announcement_date_end = models.DateTimeField('date annoucement removed')
	announcement_user = models.ForeignKey(Profile, on_delete=models.CASCADE)
	announcement_board = models.ForeignKey(Board, on_delete=models.CASCADE)

##### TYPES OF FEEDBACKS #####
class Bug(models.Model):
	id = models.AutoField(primary_key=True)
	bug_feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)
	bug_status = models.ForeignKey(Status, on_delete=models.CASCADE)

class Feature_Request(models.Model):
	id = models.AutoField(primary_key=True)
	feature_request_feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)
	feature_request_status = models.ForeignKey(Status, on_delete=models.CASCADE)

class Discussion(models.Model):
	id = models.AutoField(primary_key=True)
	discussion_feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)
	discussion_status = models.ForeignKey(Status, on_delete=models.CASCADE)

##### UNIMPLEMENTED ##### 
# Board admins should be able to create as many tags as they want for their boards
class Tag(models.Model):
	id = models.AutoField(primary_key=True)
	tag_name = models.CharField(max_length=30)
	tag_board = models.ForeignKey(Board, on_delete=models.CASCADE)
	feedback = models.ManyToManyField(Feedback)
	
	def __str__(self):
		return "%s" % self.tag_name

# Keeps track of which users voted for which feedbacks
class Vote(models.Model):
	id = models.AutoField(primary_key=True)
	vote_user = models.ForeignKey(Profile, on_delete=models.CASCADE)
	vote_feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)
	# 0 for upvote, 1 for downvote
	vote_type = models.IntegerField()

##### UNIMPLEMENTED #####
# Users should be able to follow feedbacks and tags
class Subscription(models.Model):
	id = models.AutoField(primary_key=True)
	subscription_user = models.ForeignKey(Profile, on_delete=models.CASCADE)
	subscription_feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)
	subscription_tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

class File(models.Model):
	id = models.AutoField(primary_key=True)
	file_date_uploaded = models.DateTimeField('date file uploaded')
	file_name = models.TextField()
	file_description = models.TextField()
	file_file = models.FileField()
	file_board = models.ForeignKey(Board, on_delete=models.CASCADE)
	file_user = models.ForeignKey(Profile, on_delete=models.CASCADE)
