from django.urls import path, include
from flourishapp.errorhandling import custom_404_view

# Error handing 
handler404 = custom_404_view
# handler500 = custom_500_view

urlpatterns = [

    path('dashboard/', include('flourishapp.urls.dashboard')),
    path('', include('flourishapp.urls.user.user')),
    path('employee/', include('flourishapp.urls.employee')),
    path('masters/', include('flourishapp.urls.master')),
    path('product/', include('flourishapp.urls.product')),
    path('analytics/', include('flourishapp.urls.analytics.analytics')),
    path('store/', include('flourishapp.urls.store.stock')),
    path('store/', include('flourishapp.urls.store.pos')),
    path('store/', include('flourishapp.urls.store.purchase_invoice')),
    path('settings/', include('flourishapp.urls.settings.settings')),
]