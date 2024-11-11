from flourishapp.views.store import purchase_invoice
from django.urls import path

urlpatterns = [
    path('purchase-invoice/', purchase_invoice.purchase_invoice_screen, name='purchase-invoice'),
    path('purchase-invoice-list/', purchase_invoice.purchase_invoice_list_screen, name='purchase-invoice-list'),
    path('purchase-invoice-details/', purchase_invoice.getPurchaseDetails, name='purchase-invoice-details'),
    path('delete-purchase-invoice/', purchase_invoice.deletePurchaseInvoice, name='delete-purchase-invoice'),
    path('purchase-datatable/', purchase_invoice.PurchaseDatatable, name='purchase-datatable'),
    path('purchase-product-detail/', purchase_invoice.Purchase_product_detail, name='purchase-product-detail'),
    path('get-stock-available-qty/', purchase_invoice.get_stock_available, name='get-stock-available-qty'),
    path('get-batch-no/', purchase_invoice.get_product_batch_no, name='get-batch-no'),
]