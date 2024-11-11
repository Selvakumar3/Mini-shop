from flourishapp.views import product
from django.urls import path

urlpatterns = [
   
    path('', product.product_screen, name='product'),
    path('product-list/', product.product_list_screen, name='product-list'),
    path('product-dt/', product.product_dt, name='product-dt'),
    path('edit-product/', product.edit_product, name='edit-product'),
    path('deleteproduct/', product.delete_product, name='deleteproduct'),
    path('update-product-status/', product.update_product_status, name='update-product-status'),
]