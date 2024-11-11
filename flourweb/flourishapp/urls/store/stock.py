from flourishapp.views.store import stock
from django.urls import path

urlpatterns = [
    path('stock/', stock.stock_opening_screen, name='stock'),
    path('stock_opening_dt/', stock.stock_opening_dt, name='stock_opening_dt'),
    path('deletestockopening/', stock.delete_stock_opening, name='deletestockopening'),
    path('stock_list_dt/', stock.stock_list_dt, name='stock_list_dt'),
    path('stock-list/', stock.stock_list_screen, name='stock-list'),
]
