from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('user/',include('flourishapi.urls.user')),  
    path('masters/',include('flourishapi.urls.masters')),  
    path('settings/',include('flourishapi.urls.settings')),  
    path('store/',include('flourishapi.urls.store')),  
    path('common/',include('flourishapi.urls.common')),  
    ]