from django.urls import path
from flourishapi.views.settings import *

urlpatterns = [
    path("get-billno-settings/", BillnosettingsAPI.as_view()),
    path("post-billno-settings/", BillnosettingsAPI.as_view()),
    path("get-admin-settings/", AdminSettingsAPI.as_view()),
    path("post-admin-settings/", AdminSettingsAPI.as_view()),
    path('get-email-settings/',EmailSettingsAPI.as_view()),  
    path('post-email-settings/',EmailSettingsAPI.as_view()), 
]