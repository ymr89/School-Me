from django.contrib.auth.models import Permission

# Adds all admin permissions to the specified group
def addAdminPermissions(group):
	print 'Adding admin permissions'
	changeBoard = Permission.objects.get(codename='change_board')
	deleteBoard = Permission.objects.get(codename='delete_board')
	addStatus = Permission.objects.get(codename='add_status')
	changeStatus = Permission.objects.get(codename='change_status')
	deleteStatus = Permission.objects.get(codename='delete_status')
	addFeedback = Permission.objects.get(codename='add_feedback')
	changeFeedback = Permission.objects.get(codename='change_feedback')
	deleteFeedback = Permission.objects.get(codename='delete_feedback')
	addBug = Permission.objects.get(codename='add_bug')
	changeBug = Permission.objects.get(codename='change_bug')
	deleteBug = Permission.objects.get(codename='delete_bug')
	addFeatureRequest = Permission.objects.get(codename='add_feature_request')
	changeFeatureRequest = Permission.objects.get(codename='change_feature_request')
	deleteFeatureRequest = Permission.objects.get(codename='delete_feature_request')
	addTag = Permission.objects.get(codename='add_tag')
	changeTag = Permission.objects.get(codename='change_tag')
	deleteTag = Permission.objects.get(codename='delete_tag')
	adminPermissions = [changeBoard, deleteBoard, addStatus, changeStatus, deleteStatus,
					addFeedback, changeFeedback, deleteFeedback, addBug, changeBug,
					deleteBug, addFeatureRequest, changeFeatureRequest, deleteFeatureRequest,
					addTag, changeTag, deleteTag]
	for permission in adminPermissions:
		group.permissions.add(permission)

# Adds all member permissions to the specified group
def addMemberPermissions(group):
	print 'Adding member permissions'
	changeBoard = Permission.objects.get(codename='change_board')
	deleteBoard = Permission.objects.get(codename='delete_board')
	addStatus = Permission.objects.get(codename='add_status')
	changeStatus = Permission.objects.get(codename='change_status')
	deleteStatus = Permission.objects.get(codename='delete_status')
	addFeedback = Permission.objects.get(codename='add_feedback')
	changeFeedback = Permission.objects.get(codename='change_feedback')
	deleteFeedback = Permission.objects.get(codename='delete_feedback')
	addBug = Permission.objects.get(codename='add_bug')
	changeBug = Permission.objects.get(codename='change_bug')
	deleteBug = Permission.objects.get(codename='delete_bug')
	addFeatureRequest = Permission.objects.get(codename='add_feature_request')
	changeFeatureRequest = Permission.objects.get(codename='change_feature_request')
	deleteFeatureRequest = Permission.objects.get(codename='delete_feature_request')
	addTag = Permission.objects.get(codename='add_tag')
	changeTag = Permission.objects.get(codename='change_tag')
	deleteTag = Permission.objects.get(codename='delete_tag')
	memberPermissions = [addFeedback, changeFeedback, deleteFeedback, addBug, changeBug, deleteBug,
						addFeatureRequest, changeFeatureRequest, deleteFeatureRequest]
	for permission in memberPermissions:
		group.permissions.add(permission)