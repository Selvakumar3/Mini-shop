from flourishapp.views.user import user
from django.urls import path

urlpatterns = [
    path('', user.Login, name='login'),
    path('log-out/', user.Logout, name='log-out'),
    path('forget-password/', user.forget_password_screen, name='user-forget-password'),
    path('user-reset-password/',user.reset_password, name='user-reset-password'),
    path('user-profile/',user.user_profile_screen, name='user-profile'),
    path('update-user/',user.update_display_name, name='update-user'),

    path("update-user-password/",user.update_user_password, name="update-user-password"),
    path("update-profile-picture/",user.update_profile_picture, name="update-profile-picture"),

    # usergroup urls::
    path('usergroup/', user.usergroup_screen, name='usergroup'),
	path("getusergroupmenuname/",user.GetUserGroupMenu, name="getusergroupmenuname"),
    path("usergroupdatatable/",user.GetAllUserGroup, name="usergroupdatatable"),
    path("postusergroup/",user.PostUserGroup, name="postusergroup"),
    path("deleteusergroup/",user.DeleteUserGroup, name="deleteusergroup"),
]