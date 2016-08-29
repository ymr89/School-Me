function Get(yourUrl){
    var Httpreq = new XMLHttpRequest(); // a new request
    Httpreq.open("GET", yourUrl, false);
    Httpreq.send(null);
    return Httpreq.responseText;
}
/* generic unhide function */
function unhide(divID) {
    var item = document.getElementById(divID);
    if (item) {
        item.className=(item.className=='hidden')?'unhidden':'hidden';
    }
}
/* populates and hides/unhides edit annoucement form */
function unhide_announcement(divID, ID) {
    var item = document.getElementById(divID);
    if (item) {
        item.className=(item.className=='hidden')?'unhidden':'hidden';
        var description_field = item.querySelector("#id_description")
        var newID = 'id_end_date' + ID;
        item.querySelector('#id_end_date').id = newID;
        /* datepicker functionality */
        $(function() {													  
			$( '#'+newID ).datepicker({
		      changeMonth: true,
		      changeYear: true,
		    });
		  })
        var json_obj = JSON.parse(Get('/api/announcements/' + ID + '/'));
        var key = parseInt(ID);
        //console.log(json_obj);
        var Description = (json_obj.announcement_description);
        description_field.value = Description;
    }
}


/* populates and hides/unhides edit feedback form */
function unhide_feedback(divID, FeedbackID, userID) {
    var item = document.getElementById(divID);
    if (item) {
        item.className=(item.className=='hidden')?'unhidden':'hidden';
        var title_field = item.querySelector("#id_title")
        var body_field = item.querySelector("#id_body")
        var json_obj = JSON.parse(Get('/api/feedbacks/' + FeedbackID + '/' + userID + '/'));
        var key = parseInt(FeedbackID);
        console.log(json_obj);
        var FeedbackTitle = (json_obj.feedback_title);
        var FeedbackDescription = (json_obj.feedback_description);
        title_field.value = FeedbackTitle;
        body_field.value = FeedbackDescription;
        var commentItem = document.getElementById('wrap_write_comment');
        if(commentItem) {
            if(commentItem.style.display !== 'none') {
                commentItem.style.display = 'none';
            }
        }
    }
}
/* populates and hides/unhides edit comment form */
function unhide_comment(divID, comment_id) {
    var item = document.getElementById(divID);
    if (item) {
        item.className=(item.className=='hidden')?'unhidden':'hidden';
        var field = item.querySelector("#id_comment")
        var json_obj = JSON.parse(Get('/api/comments/' + comment_id + '/'));
        var key = parseInt(comment_id);
        console.log(json_obj);
        var content = (json_obj.comment);
        field.value = content;
        var commentItem = document.getElementById('wrap_write_reply_' + comment_id);
        if(commentItem) {
            if(commentItem.style.display !== 'none') {
                commentItem.style.display = 'none';
            }
        }
    }
}
/* filter button functionality on board home and discussion pages */
function filter(fieldID, valueToSelect) {
    var item = document.getElementById(fieldID);
    console.log(item);
    if (item) {
        item.value = valueToSelect;
        document.ff.submit();
    }
}
/* fills in edit profile form on edit page */
function edit_profile(userID) {
    var orgField = document.getElementById('id_organization');
    var emailField = document.getElementById('id_email');
    var firstField = document.getElementById('id_first');
    var lastField = document.getElementById('id_last');
    var user_obj = JSON.parse(Get('/api/users/' + userID + '/'));
    var profile_obj = JSON.parse(Get('/api/profiles/' + userID + '/'));
    firstField.value = (user_obj.first_name);
    lastField.value = (user_obj.last_name);
    emailField.value = (user_obj.email);
    var orgID = (profile_obj.user_organization);
    var org_obj = JSON.parse(Get('/api/organizations/' + orgID + '/'));
    orgField.value = (org_obj.organization_name);
}
/* create board form dropdown buttons */
function privacy_control(fieldID, value) {
    var choice = document.getElementById(fieldID);
    choice.value = value;
    var butt = $("#dropButton"); //document.getElementById('dropButton');
    console.log(butt.html());
	 if (value == '0') {    
    	butt.html('Public <span class="caret"></span>')
    }
    else {
		butt.html('Private <span class="caret"></span>')    
    }
}
function create_board() {
	var form_field = document.getElementById('id_board_name');
	form_field.value = document.getElementById('fake_field').value;
	document.cbf.submit();
}