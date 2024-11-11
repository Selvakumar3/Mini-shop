from django.urls import path
from flourishapi.views.store import *

urlpatterns = [

    # Stock opening
    path("post-stockopening/", StockOpeningAPI.as_view(),name="post-stockopening"),
    path("delete-stockopening/", StockOpeningDeleteAPI.as_view(),name="post-stockopening"),
    path("stockopening-dt/", StockOpeningDataTableAPI.as_view(),name="stockopening-dt"),
    path("get-stock-qty/", GetAvailableStockAgainstBatchAPI.as_view(),name="get-stock-qty"),
    path("get-stock-dt/", StockDatatableAPI.as_view(),name="get-stock-dt"),

    # Purchase invoice
    path("post-purchase-invoice/", PurchaseApi.as_view(),name="post-purchase-invoice"),
    path("purchasedet-detail/", PurchaseDetDetailAPI.as_view(),name="purchasedet-detail"),
    path("get-purchase-edit/", UpdatePurchaseAPI.as_view(), name="get-purchase-edit"),
    path("update-purchase-invoice/", UpdatePurchaseAPI.as_view(), name="update-purchase-invoice"),
    path("delete-purchase-invoice/", UpdatePurchaseAPI.as_view(), name="delete-purchase-invoice"),
    path("purchase-dt/", PurchaseDatatableAPI.as_view(), name="purchase-dt"),
    path("get-product-batch/", GetProductAgainstBatchAPI.as_view(), name="get-product-batch"),

    # POS
    path("post-pos/", CreatePOSApi.as_view(),name="post-pos"),
    path("posdet-detail/", PosDetDetailAPI.as_view(),name="posdet-detail"),
    path("get-pos-edit/", UpdatePosAPI.as_view(), name="get-pos-edit"),
    path("update-pos/", UpdatePosAPI.as_view(), name="update-pos"),
    path("delete-pos/", UpdatePosAPI.as_view(), name="delete-pos"),
    path("pos-dt/", PosDatatableAPI.as_view(), name="pos-dt"),
   
]