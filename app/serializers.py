from rest_framework import serializers
from .models import Email_Token, Announcement, Organization, Board, Profile, Status, Feedback, Bug, Feature_Request, Discussion, Tag, Vote, Subscription, Comment, File

from django.contrib.auth.models import User, Group

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'first_name', 'last_name', 'groups', 'user_permissions', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined')

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('id', 'board_name', 'groups')

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'permissions')

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'organization_name')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
    	model = Profile
    	fields = ('id', 'user','user_organization', 'boards')

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
    	model = Status
    	fields = ('id', 'status_name', 'status_board')

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
    	model = Feedback
    	fields = ('id', 'feedback_title', 'feedback_description', 'feedback_date_created', 'feedback_last_modified', 'feedback_user', 'feedback_board', 'feedback_status', 'feedback_upvotes', 'feedback_downvotes')

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ('id', 'announcement_description', 'announcement_date_created', 'announcement_last_modified', 'announcement_user', 'announcement_board')

class BugSerializer(serializers.ModelSerializer):
    class Meta:
    	model = Bug
    	fields = ('id', 'bug_feedback', 'bug_status')

class Feature_RequestSerializer(serializers.ModelSerializer):
    class Meta:
    	model = Feature_Request
    	fields = ('id', 'feature_request_feedback', 'feature_request_status')

class DiscussionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discussion
        fields = ('id', 'discussion_feedback', 'discussion_status')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
    	model = Tag
    	fields = ('id', 'tag_name', 'tag_board', 'feedback')

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
    	model = Vote
    	fields = ('id', 'vote_user', 'vote_feedback', 'vote_type')

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
    	model = Subscription
    	fields = ('id', 'subscription_user', 'subscription_feedback', 'subscription_tag')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
    	model = Comment
    	fields = ('id', 'object_pk', 'user_name', 'user_email', 'user_url', 'comment', 'submit_date', 'ip_address', 'is_public', 'is_removed', 'content_type', 'site', 'user')

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'file_date_uploaded', 'file_name', 'file_description', 'file_file', 'file_board', 'file_user')   

class Email_TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email_Token
        fields = ('id', 'email', 'token') 