from django.urls import path 
from flourishapi.views import user

urlpatterns = [
    
    path('login/',user.LoginAPI.as_view(),name='login'),
    path('v1/auth/logout/', user.LogoutAPI.as_view(), name='user_logout'),
    path('user-forgot-password/',user.ResetPasswordRequestEmailAPI.as_view()),
    path('password-reset-confirm/<uidb64>/<token>/',user.PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'), 
    path('get-profile/', user.UserProfileUpdate.as_view()),
    path('update-profile/', user.UserProfileUpdate.as_view()),
    path('user-password-update/', user.UserPasswordUpdateAPI.as_view(), name='user-password-update'),
    path('update-userprofile-picture/',user.UserProfileImgeUpdateAPI.as_view(), name='update-userprofile-picture'),
    path('get-userprofile-picture/',user.UserProfileImgeUpdateAPI.as_view(), name='get-userprofile-picture'),

]