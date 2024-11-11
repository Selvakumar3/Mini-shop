from flourishapp.views import dashboard
from django.urls import path

urlpatterns = [
    path('', dashboard.dashboard, name='dashboard'),
]