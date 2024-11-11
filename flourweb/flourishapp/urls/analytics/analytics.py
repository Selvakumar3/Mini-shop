from flourishapp.views.analytics import analytics
from django.urls import path

urlpatterns = [
    path('', analytics.analytics_screen, name='analytics'),
]