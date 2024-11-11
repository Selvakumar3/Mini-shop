from .models import *

def MenuCreation():
    Menu.objects.bulk_create([
        Menu(menu_id=1, menu_name="Dashboard", url="/dashboard/", file_name="dashboard.html", icon_path="menu-icon mdi mdi-view-dashboard dashboard-icon", parent_id=None, row_index=0, is_module=True, is_visible=True, description="dashboard", is_administrator=True),
        Menu(menu_id=2, menu_name="User", url="/dashboard/", file_name="#", icon_path="menu-icon mdi mdi-account-circle-outline", parent_id=None, row_index=100, is_module=True, is_visible=True, description="User", is_administrator=True),
        Menu(menu_id=3, menu_name="Employee", url="/dashboard/", file_name="#", icon_path="menu-icon mdi mdi-account-tie master-icon", parent_id=None, row_index=200, is_module=True, is_visible=True, description="Employee", is_administrator=True),
        Menu(menu_id=4, menu_name="Masters", url="/dashboard/", file_name="#", icon_path="menu-icon mdi mdi-monitor screen-icon", parent_id=None, row_index=300, is_module=True, is_visible=True, description="Masters", is_administrator=True),
        Menu(menu_id=5, menu_name="Products", url="/dashboard/", file_name="#", icon_path="menu-icon mdi mdi-package-variant product-icon", parent_id=None, row_index=400, is_module=True, is_visible=True, description="Products", is_administrator=True),
        Menu(menu_id=6, menu_name="Store", url="/dashboard/", file_name="#", icon_path="menu-icon mdi mdi-store store-icon", parent_id=None, row_index=500, is_module=True, is_visible=True, description="Store", is_administrator=True),
        Menu(menu_id=7, menu_name="Billing", url="/dashboard/", file_name="#", icon_path="menu-icon mdi mdi-file-document-outline invoice-icon", parent_id=None, row_index=600, is_module=True, is_visible=True, description="Billing", is_administrator=True),
        Menu(menu_id=8, menu_name="Visual", url="/dashboard/", file_name="#", icon_path="menu-icon mdi mdi-chart-line chart-icon", parent_id=None, row_index=700, is_module=True, is_visible=True, description="Visual", is_administrator=True),
        Menu(menu_id=9, menu_name="Settings", url="/dashboard/", file_name="#", icon_path="menu-icon mdi mdi-cog settings-icon", parent_id=None, row_index=800, is_module=True, is_visible=True, description="Settings", is_administrator=True),
       
        # User ::
        Menu(menu_id=10, menu_name="Usergroup", url="/usergroup/", file_name="#", icon_path="#", parent_id=2, row_index=101, is_module=False, is_visible=True, description="Usergroup", is_administrator=True),

        # Employee ::
        Menu(menu_id=11, menu_name="Employee", url="/employee/", file_name="#", icon_path="#", parent_id=3, row_index=201, is_module=False, is_visible=True, description="Employee", is_administrator=True),
        Menu(menu_id=12, menu_name="Employee List", url="/employee/employee-list/", file_name="#", icon_path="#", parent_id=3, row_index=202, is_module=False, is_visible=True, description="Employee List", is_administrator=True),

        # Masters ::
        Menu(menu_id=13, menu_name="Category", url="/masters/category/", file_name="#", icon_path="#", parent_id=4, row_index=301, is_module=False, is_visible=True, description="Category", is_administrator=True),
        Menu(menu_id=14, menu_name="Brand", url="/masters/brand/", file_name="#", icon_path="#", parent_id=4, row_index=302, is_module=False, is_visible=True, description="Brand", is_administrator=True),
        Menu(menu_id=15, menu_name="Unit", url="/masters/unit/", file_name="#", icon_path="#", parent_id=4, row_index=303, is_module=False, is_visible=True, description="Unit", is_administrator=True),

        # Products ::
        Menu(menu_id=16, menu_name="Product", url="/product/", file_name="#", icon_path="#", parent_id=5, row_index=401, is_module=False, is_visible=True, description="Product", is_administrator=True),
        Menu(menu_id=17, menu_name="Product List", url="/product/product-list/", file_name="#", icon_path="#", parent_id=5, row_index=402, is_module=False, is_visible=True, description="Product List", is_administrator=True),

        # Store ::
        Menu(menu_id=18, menu_name="Stock opening", url="/store/stock/", file_name="#", icon_path="#", parent_id=6, row_index=501, is_module=False, is_visible=True, description="Stock opening", is_administrator=True),
        Menu(menu_id=19, menu_name="Stock list", url="/store/stock-list/", file_name="#", icon_path="#", parent_id=6, row_index=502, is_module=False, is_visible=True, description="Stock list", is_administrator=True),
        Menu(menu_id=20, menu_name="POS", url="/store/point-on-sale/", file_name="#", icon_path="#", parent_id=6, row_index=503, is_module=False, is_visible=True, description="POS", is_administrator=True),
        Menu(menu_id=21, menu_name="POS List", url="/store/pos-list/", file_name="#", icon_path="#", parent_id=6, row_index=504, is_module=False, is_visible=True, description="POS List", is_administrator=True),

        # Billing ::
        Menu(menu_id=22, menu_name="Purchase invoice", url="/store/purchase-invoice/", file_name="#", icon_path="#", parent_id=7, row_index=601, is_module=False, is_visible=True, description="Purchase invoice", is_administrator=True),
        Menu(menu_id=23, menu_name="Purchase invoice List", url="/store/purchase-invoice-list/", file_name="#", icon_path="#", parent_id=7, row_index=602, is_module=False, is_visible=True, description="Purchase invoice List", is_administrator=True),

        # Visual ::
        Menu(menu_id=24, menu_name="Visual", url="/analytics/", file_name="#", icon_path="#", parent_id=8, row_index=701, is_module=False, is_visible=True, description="Visual", is_administrator=True),

        # Settings ::
        Menu(menu_id=25, menu_name="Admin config", url="/settings/", file_name="#", icon_path="#", parent_id=9, row_index=801, is_module=False, is_visible=True, description="Admin config", is_administrator=True),
        Menu(menu_id=26, menu_name="Billno settings", url="/settings/billno-settings/", file_name="#", icon_path="#", parent_id=9, row_index=802, is_module=False, is_visible=True, description="Billno settings", is_administrator=True),
        Menu(menu_id=26, menu_name="Logs", url="/settings/log-list/", file_name="#", icon_path="#", parent_id=9, row_index=803, is_module=False, is_visible=True, description="Logs", is_administrator=True),
    ])

def BillTypeCreation():
    BillType.objects.bulk_create([
        BillType(bill_typeid=1,bill_type = 'Cash'),
        BillType(bill_typeid=2,bill_type = 'UPI'),
    ])
