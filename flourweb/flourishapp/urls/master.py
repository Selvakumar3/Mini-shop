from flourishapp.views import master
from django.urls import path

urlpatterns = [

    # Category urls ::
    path('category/', master.category_screen, name='category'),
    path('category-dt/', master.category_dt, name='category-dt'),
    path('edit-category/', master.edit_category, name='edit-category'),
    path('deletecategory/', master.delete_category, name='deletecategory'),
    path('update-category-status/', master.update_category_status, name='update-category-status'),

    # Brand urls ::
    path('brand/', master.brand_screen, name='brand'),
    path('brand-dt/', master.brand_dt, name='brand-dt'),
    path('edit-brand/', master.edit_brand, name='edit-brand'),
    path('deletebrand/', master.delete_brand, name='deletebrand'),
    path('update-brand-status/', master.update_brand_status, name='update-brand-status'),

    path('unit/', master.unit_screen, name='unit'),
    path('unit-dt/', master.unit_dt, name='unit-dt'),
    path('edit-unit/', master.edit_unit, name='edit-unit'),
    path('deleteunit/', master.delete_unit, name='deleteunit'),
   
]