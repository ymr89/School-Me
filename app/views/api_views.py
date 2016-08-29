from app.models import File, Email_Token, Discussion, Announcement, Organization, Board, Profile, Status, Feedback, Bug, Feature_Request, Tag, Vote, Subscription, Comment
from app.serializers import Email_TokenSerializer, DiscussionSerializer, AnnouncementSerializer, GroupSerializer, BoardSerializer, OrganizationSerializer, ProfileSerializer, VoteSerializer, StatusSerializer, FeedbackSerializer, BugSerializer, Feature_RequestSerializer, TagSerializer, SubscriptionSerializer, CommentSerializer, UserSerializer, FileSerializer
from django.contrib.auth.models import User, Group, Permission
from rest_framework import permissions, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse


"""Creates endpoint for root of API """
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def api_root(request, format=None):
	return Response({
		'profiles': reverse('profile-list', request=request, format=format),
		'organizations': reverse('organization-list', request=request, format=format),
		'boards': reverse('board-list', request=request, format=format),
		'groups': reverse('group-list', request=request, format=format),
		'statuses': reverse('status-list', request=request, format=format),
		'feedbacks': reverse('feedback-list', request=request, format=format),
		'announcements': reverse('announcement-list', request=request, format=format),
		'bugs': reverse('bug-list', request=request, format=format),
		'feature_requests': reverse('feature_request-list', request=request, format=format),
		'tags': reverse('tag-list', request=request, format=format),
		'votes': reverse('vote-list', request=request, format=format),
		'subscriptions': reverse('subscription-list', request=request, format=format),
		'comments': reverse('comment-list', request=request, format=format),
		'discussions': reverse('discussion-list', request=request, format=format),
		'users': reverse('user-list', request=request, format=format),
		'email_tokens': reverse('email-token-list', request=request, format=format),
		'files': reverse('file-list', request=request, format=format),
		})

# API views for each model
@permission_classes((permissions.AllowAny,))
class board_list(generics.ListCreateAPIView):
	"""List boards or create a new one"""
	queryset = Board.objects.all()
	serializer_class = BoardSerializer

@permission_classes((permissions.AllowAny,))
class board_detail(generics.RetrieveUpdateDestroyAPIView):
	"""Retrieve, update or delete a board"""
	queryset = Board.objects.all()
	serializer_class = BoardSerializer

@permission_classes((permissions.AllowAny,))
class profile_list(generics.ListCreateAPIView):
	"""List profiles or create a new one"""
	queryset = Profile.objects.all()
	serializer_class = ProfileSerializer

@permission_classes((permissions.AllowAny,))
class profile_detail(generics.RetrieveUpdateDestroyAPIView):
	"""Retrieve, update or delete a profile"""
	queryset = Profile.objects.all()
	serializer_class = ProfileSerializer

@permission_classes((permissions.AllowAny,))
class group_list(generics.ListCreateAPIView):
	"""List groups or create a new one"""
	queryset = Group.objects.all()
	serializer_class = GroupSerializer

@permission_classes((permissions.AllowAny,))
class group_detail(generics.RetrieveUpdateDestroyAPIView):
	"""Retrieve, update or delete a group"""
	queryset = Group.objects.all()
	serializer_class = GroupSerializer

@permission_classes((permissions.AllowAny,))
class organization_list(generics.ListCreateAPIView):
	"""List organizations or create a new one"""
	queryset = Organization.objects.all()
	serializer_class = OrganizationSerializer

@permission_classes((permissions.AllowAny,))
class organization_detail(generics.RetrieveUpdateDestroyAPIView):
	"""Retrieve, update or delete an organization"""
	queryset = Organization.objects.all()
	serializer_class = OrganizationSerializer

@permission_classes((permissions.AllowAny,))
class status_list(generics.ListCreateAPIView):
	"""List statuses or create a new one"""
	queryset = Status.objects.all()
	serializer_class = StatusSerializer

@permission_classes((permissions.AllowAny,))
class status_detail(generics.RetrieveUpdateDestroyAPIView):
	"""Retrieve, update or delete a status"""
	queryset = Status.objects.all()
	serializer_class = StatusSerializer

@permission_classes((permissions.AllowAny,))
class feedback_list(generics.ListCreateAPIView):
	"""List feedbacks or create a new one"""
	queryset = Feedback.objects.all()
	serializer_class = FeedbackSerializer

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((permissions.AllowAny,))
def feedback_detail(request, pk, feedbackuserid, format=None):
	"""Retrieve update or delete a feedback"""
	
	# if user calling the http request is not the current logged in user, HTTP400
	if int(feedbackuserid) != request.user.profile.id:
		return Response(status=status.HTTP_400_BAD_REQUEST)

	try:
		feedback = Feedback.objects.get(pk=pk)
	except Feedback.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = FeedbackSerializer(feedback)
		return Response(serializer.data)

	elif request.method == 'PUT':
		serializer = FeedbackSerializer(feedback, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	elif request.method == 'DELETE':
		feedback.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

@permission_classes((permissions.AllowAny,))
class user_list(generics.ListCreateAPIView):
	"""List users or create a new one"""
	queryset = User.objects.all()
	serializer_class = UserSerializer

@permission_classes((permissions.AllowAny,))
class user_detail(generics.RetrieveUpdateDestroyAPIView):
	"""Retrieve, update or delete a user"""
	queryset = User.objects.all()
	serializer_class = UserSerializer

@permission_classes((permissions.AllowAny,))
class announcement_list(generics.ListCreateAPIView):
	"""List statuses or create a new one"""
	queryset = Announcement.objects.all()
	serializer_class = AnnouncementSerializer

@permission_classes((permissions.AllowAny,))
class announcement_detail(generics.RetrieveUpdateDestroyAPIView):
	"""Retrieve, update or delete a status"""
	queryset = Announcement.objects.all()
	serializer_class = AnnouncementSerializer

# @permission_classes((permissions.AllowAny,))
# class feedback_detail(generics.RetrieveUpdateDestroyAPIView):
# 	"""Retrieve, update or delete a feedback"""
# 	queryset = Feedback.objects.all()
# 	serializer_class = FeedbackSerializer

@permission_classes((permissions.AllowAny,))
class bug_list(generics.ListCreateAPIView):
	"""List bugs or create a new one"""
	queryset = Bug.objects.all()
	serializer_class = BugSerializer

@permission_classes((permissions.AllowAny,))
class bug_detail(generics.RetrieveUpdateDestroyAPIView):
	"""Retrieve, update or delete a bug"""
	queryset = Bug.objects.all()
	serializer_class = BugSerializer

@permission_classes((permissions.AllowAny,))
class feature_request_list(generics.ListCreateAPIView):
	"""List feature requests or create a new one"""
	queryset = Feature_Request.objects.all()
	serializer_class = Feature_RequestSerializer

@permission_classes((permissions.AllowAny,))
class feature_request_detail(generics.RetrieveUpdateDestroyAPIView):
	"""Retrieve, update or delete a feature request"""
	queryset = Feature_Request.objects.all()
	serializer_class = Feature_RequestSerializer

@permission_classes((permissions.AllowAny,))
class discussion_list(generics.ListCreateAPIView):
	"""List feature requests or create a new one"""
	queryset = Discussion.objects.all()
	serializer_class = DiscussionSerializer

@permission_classes((permissions.AllowAny,))
class discussion_detail(generics.RetrieveUpdateDestroyAPIView):
	"""Retrieve, update or delete a feature request"""
	queryset = Discussion.objects.all()
	serializer_class = DiscussionSerializer

@permission_classes((permissions.AllowAny,))
class tag_list(generics.ListCreateAPIView):
	"""List tags or create a new one"""
	queryset = Tag.objects.all()
	serializer_class = TagSerializer

@permission_classes((permissions.AllowAny,))
class tag_detail(generics.RetrieveUpdateDestroyAPIView):
	"""Retrieve, update or delete a tag"""
	queryset = Tag.objects.all()
	serializer_class = TagSerializer

@permission_classes((permissions.AllowAny,))
class vote_list(generics.ListCreateAPIView):
	"""List votes or create a new one"""
	queryset = Vote.objects.all()
	serializer_class = VoteSerializer

@permission_classes((permissions.AllowAny,))
class vote_detail(generics.RetrieveUpdateDestroyAPIView):
	"""Retrieve, update or delete a vote"""
	queryset = Vote.objects.all()
	serializer_class = VoteSerializer

@permission_classes((permissions.AllowAny,))
class subscription_list(generics.ListCreateAPIView):
	"""List subscriptions or create a new one"""
	queryset = Subscription.objects.all()
	serializer_class = SubscriptionSerializer

@permission_classes((permissions.AllowAny,))
class subscription_detail(generics.RetrieveUpdateDestroyAPIView):
	"""Retrieve, update or delete a subscription"""
	queryset = Subscription.objects.all()
	serializer_class = SubscriptionSerializer

@permission_classes((permissions.AllowAny,))
class comment_list(generics.ListCreateAPIView):
	"""List comments or create a new one"""
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer

@permission_classes((permissions.AllowAny,))
class comment_detail(generics.RetrieveUpdateDestroyAPIView):
	"""Retrieve, update or delete a comment"""
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer

@permission_classes((permissions.AllowAny,))
class file_list(generics.ListCreateAPIView):
	"""List files or create a new one"""
	queryset = File.objects.all()
	serializer_class = FileSerializer

@permission_classes((permissions.AllowAny,))
class file_detail(generics.RetrieveUpdateDestroyAPIView):
	"""Retrieve, update or delete a file"""
	queryset = File.objects.all()
	serializer_class = FileSerializer

@permission_classes((permissions.AllowAny,))
class email_token_list(generics.ListCreateAPIView):
	"""List email_token or create a new one"""
	queryset = Email_Token.objects.all()
	serializer_class = Email_TokenSerializer

@permission_classes((permissions.AllowAny,))
class email_token_detail(generics.RetrieveUpdateDestroyAPIView):
	"""Retrieve, update or delete a email_token"""
	queryset = Email_Token.objects.all()
	serializer_class = Email_TokenSerializer