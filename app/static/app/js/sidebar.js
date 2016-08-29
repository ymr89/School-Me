function Sidebar(user, id){
document.getElementById("navMenu").innerHTML =
 '<a href="/profile/'+id+'" style="text-decoration: none; color: white;"><div id="circle"><span class="glyphicon glyphicon-user"></span></div><h2>' + user + '</h2></a>'+
 '<ul class="nav nav-pills nav-stacked" style="text-align: left;">'+
  '<li><a href="/userhome/" class="asidebar"><i class="fa fa-newspaper-o fa-fw" aria-hidden="true"></i>&nbsp;  Feed</a></li>'+
  '<li><a href="/profile/'+id+'" class="asidebar"><i class="fa fa-user fa-fw" aria-hidden="true"></i>&nbsp;  Profile</a></li>'+
  '<li><a href="/messages/" class="asidebar"><i class="fa fa-envelope fa-fw" aria-hidden="true"></i>&nbsp;  Messages</a></li>'+
  '<li><a href="/boards/" class="asidebar"><i class="fa fa-users fa-fw" aria-hidden="true"></i>&nbsp;  Boards</a></li>'+
  '<li><a href="#" class="asidebar"><label for="logout" style="font-size: inherit; font-weight: inherit;"><i class="fa fa-lock fa-fw" aria-hidden="true"></i>&nbsp;  Logout</label></a></li>'+
 '</ul>';
}