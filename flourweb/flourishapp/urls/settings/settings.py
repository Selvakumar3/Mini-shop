from flourishapp.views.settings import settings
from django.urls import path

urlpatterns = [
    path('', settings.Settings_screen, name='settings'),
    path('billno-settings/', settings.billno_Settings_screen, name='billno-settings'),
    path('update-admin-settings/', settings.update_admin_setting, name='update-admin-settings'),
    path('update-email-settings/', settings.update_email_setting, name='update-email-settings'),
    path('log-list/', settings.log_list_screen, name='log-list'),
    path('log_list_dt/', settings.log_screen, name='log_list_dt'),
    
]