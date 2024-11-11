from flourishapp.views.store import pos
from django.urls import path

urlpatterns = [
    path('point-on-sale/', pos.pos_screen, name='pos'),
    path('pos-list/', pos.pos_list_screen, name='pos-list'),
    path('pos-details/', pos.getPosDetails, name='pos-details'),
    path('delete-pos/', pos.deletePos, name='delete-pos'),
    path('pos-datatable/', pos.PosDatatable, name='pos-datatable'),
]