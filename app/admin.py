from django.contrib import admin
from .models import Discussion, Organization, Announcement, Profile, Board, Status, Feedback, Bug, Feature_Request, Tag, Vote, Subscription, Comment
from django.contrib.auth.models import User, Group

# Register your models here.
admin.site.register(Organization)
admin.site.register(Profile)
admin.site.register(Board)
admin.site.register(Status)
admin.site.register(Feedback)
admin.site.register(Bug)
admin.site.register(Feature_Request)
admin.site.register(Tag)
admin.site.register(Vote)
admin.site.register(Subscription)
admin.site.register(Comment)
admin.site.register(Announcement)
admin.site.register(Discussion)