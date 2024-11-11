from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from datetime import timedelta

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **kwargs):
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email_id=None, password=None, **kwargs):
        user = self.create_user(
            username=username,
            email_id=email_id,
            password=password,
            is_super_admin=True,
            is_admin=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=100,unique=True,null=True, blank=True, error_messages={'unique':'Username already exists'})
    display_name = models.CharField(max_length=100,null=True, blank=True)
    mobile_number = models.CharField(max_length=10,null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    profile_image = models.ImageField(upload_to='user/profile/', null=True, blank=True) 
    email_verified_at = models.DateTimeField(null=True, blank=True)
    mobile_verified_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    otp = models.CharField(max_length=250, null=True)
    otp_expiry_datetime = models.DateTimeField(null=True, blank=True)
    otp_expired = models.BooleanField(default=False,null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    account_holder_name = models.CharField(max_length=100, null=True, blank=True)
    account_no = models.CharField(max_length=20, unique=True, null=True, blank=True)
    ifsc_code = models.CharField(max_length=30,null=True, blank=True)
    bank_name = models.CharField(max_length=200, null=True, blank=True)
    branch_name = models.CharField(max_length=200, null=True, blank=True)
    dateOf_birth = models.DateField(null=True, blank=True)
    usergroup = models.ForeignKey('UserGroup', on_delete=models.RESTRICT, null=True, blank=True, related_name="user_group_id")
    is_super_admin = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL,null=True, blank=True, related_name='usercreate_user_id')  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_by = models.ForeignKey("User", on_delete=models.SET_NULL,null=True, blank=True, related_name='userupdate_user_id')  
    updated_at = models.DateTimeField(null=True, blank=True)  
   
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['mobile_number']

    def has_perm(self, perm, obj=None):
        return self.is_super_admin

    def has_module_perms(self, app_label):
        return self.is_super_admin

    def __str__(self):
        return self.username

class Logs(models.Model):
    log_id = models.BigAutoField(primary_key=True, editable=False)
    transaction_name = models.CharField(max_length=250)
    mode = models.CharField(max_length=100)
    log_message = models.TextField()
    user = models.ForeignKey('User', on_delete=models.RESTRICT, null=True, blank=True, related_name="user_id")
    Ip_address = models.CharField(max_length=100, null=True, blank=True)
    system_name = models.CharField(max_length=100, null=True, blank=True)
    log_date = models.DateTimeField()
    log_type = models.CharField(max_length=100)
    
    def __str__(self):
        return self.transaction_name  
    
class BlockedToken(models.Model):
    token_id = models.BigAutoField(primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_block_token')
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class UserGroup(models.Model):
    usergroup_id = models.BigAutoField(primary_key=True, editable=False)
    usergroup_name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT,null=True, blank=True, related_name='usergroup_created_id' )    
    created_date = models.DateTimeField(auto_now=True, null=True, blank=True,)
    updated_by = models.ForeignKey(User, on_delete=models.RESTRICT,null=True, blank=True, related_name='usergroup_updated_id')    
    updated_at = models.DateTimeField(null=True, blank=True)

class UserGroupMenu(models.Model):
    usergroup_menu_id = models.BigAutoField(primary_key=True, editable=False)
    usergroup = models.ForeignKey(UserGroup, on_delete=models.RESTRICT, related_name="usergroupid")
    menu = models.ForeignKey('Menu', on_delete=models.RESTRICT, null=True, blank=True, related_name="menuid")

class Menu(models.Model):
    menu_id = models.IntegerField(primary_key=True, editable=False)
    menu_name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    file_name = models.CharField(max_length=100)
    icon_path = models.CharField(max_length=100)
    parent_id = models.IntegerField(null=True, blank=True)
    row_index = models.IntegerField(null=True, blank=True)
    is_module = models.BooleanField(default=True)
    is_visible = models.BooleanField(default=True)
    description = models.CharField(max_length=100,null=True, blank=True)
    is_administrator = models.BooleanField(default=True)

class RolePermission(models.Model):
    role_permission_id = models.BigAutoField(primary_key=True, editable=False)
    menu = models.ForeignKey('Menu', on_delete=models.RESTRICT, null=True, blank=True, related_name="role_permission_menu_id")
    
class Category(models.Model):
    categoryid = models.BigAutoField(primary_key=True, editable=False)
    category_name = models.CharField(max_length=100)
    category_desc = models.TextField(null=True, blank=True)
    category_image = models.ImageField(upload_to="category", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        "User",
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="cat_created_by",
    )
    created_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        "User",
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="cat_updated_by",
    )
    updated_at = models.DateTimeField(null=True, blank=True)

class Brand(models.Model):
    brand_id = models.BigAutoField(primary_key=True, editable=False)
    brand_name = models.CharField(max_length=100)
    brand_image = models.ImageField(upload_to='brand/brandImage/', null=True, blank=True) 
    category = models.ForeignKey('Category', on_delete=models.RESTRICT, null=True, blank=True, related_name="brand_category_id")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('User', on_delete=models.RESTRICT, null=True, blank=True, related_name="brand_created_by")
    updated_by = models.ForeignKey('User', on_delete=models.RESTRICT, null=True, blank=True, related_name="brand_updated_by")
    updated_at = models.DateTimeField(null=True, blank=True)
  
class Unit(models.Model):
    unit_id = models.BigAutoField(primary_key=True, editable=False)
    unit_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    convertion_value = models.IntegerField(default=1)
    created_by = models.ForeignKey('User', on_delete=models.RESTRICT, null=True, blank=True, related_name="unit_created_by")
    created_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('User', on_delete=models.RESTRICT, null=True, blank=True, related_name="unit_updated_by")
    updated_at = models.DateTimeField(null=True, blank=True)
   
class Product(models.Model):
    product_id = models.BigAutoField(primary_key=True, editable=False)
    product_name = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.RESTRICT, null=True, blank=True, related_name="product_category_id")
    brand = models.ForeignKey('Brand', on_delete=models.RESTRICT, null=True, blank=True, related_name="product_brand_id")
    unit = models.ForeignKey('Unit', on_delete=models.RESTRICT, null=True, blank=True, related_name="product_unit_id")
    product_image = models.ImageField(upload_to='product/productImage/', null=True, blank=True)
    mrp = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    customer_price = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    desc = models.TextField(null=True, blank=True)
    sales_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey('User', on_delete=models.RESTRICT, null=True, blank=True, related_name="product_created_by")
    created_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('User', on_delete=models.RESTRICT, null=True, blank=True, related_name="product_updated_by")
    updated_at = models.DateTimeField(null=True, blank=True)

class Employee(models.Model):
    employee_id = models.BigAutoField(primary_key=True, editable=False)
    employee_no = models.CharField(max_length=100,null=True, blank=True)
    first_name = models.CharField(max_length=100,null=True, blank=True)
    last_name = models.CharField(max_length=100,null=True, blank=True)
    doj = models.DateTimeField(null=True, blank=True)
    mobile_number = models.CharField(max_length=10,null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    employee_image = models.ImageField(upload_to='employee/employeeImage/', null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    username = models.CharField(max_length=100,unique=True,null=True, blank=True, error_messages={'unique':'Username already exists'})
    usergroup = models.ForeignKey(UserGroup, on_delete=models.RESTRICT, related_name="employee_usergroupid")
    is_active = models.BooleanField(default=True)
    emp_user = models.ForeignKey('User', on_delete=models.RESTRICT, null=True, blank=True, related_name="employee_userid")
    created_by = models.ForeignKey('User', on_delete=models.RESTRICT, null=True, blank=True, related_name="employee_created_by")
    created_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('User', on_delete=models.RESTRICT, null=True, blank=True, related_name="employee_updated_by")
    updated_at = models.DateTimeField(null=True, blank=True)
   
class BillnoSettings(models.Model):
    billno_id = models.BigAutoField(primary_key=True, editable=False)
    user = models.ForeignKey('User', on_delete=models.RESTRICT, related_name="billnosetting_userid")
    employee_prefix = models.CharField(max_length=100, null=True, blank=True)
    employee_length = models.IntegerField(default=0)
    employee_live = models.IntegerField(default=0)
    bat_prefix = models.CharField(max_length=50,null=True, blank=True)
    bat_length = models.IntegerField(default=0,null=True, blank=True)
    bat_live = models.IntegerField(default=0,null=True, blank=True)
    inv_prefix = models.CharField(max_length=100, null=True, blank=True)
    inv_length = models.IntegerField(default=0)
    inv_live = models.IntegerField(default=0)
    pur_prefix = models.CharField(max_length=100, null=True, blank=True)
    pur_length = models.IntegerField(default=0)
    pur_live = models.IntegerField(default=0)
    
class AdminSettings(models.Model):
    admin_settingsid = models.BigAutoField(primary_key=True, editable=False)
    otp_length = models.IntegerField(default=0)
    otp_expiry_duration = models.IntegerField(default=0)
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True, related_name='admin_config_userid')
    is_maintenance_mode = models.BooleanField(default=False)
    company_name = models.CharField(max_length=255,blank=True, null=True)
    company_contact_no = models.CharField(max_length=20,blank=True, null=True)
    company_email = models.EmailField(unique=True, null=True)
    company_address = models.CharField(max_length=255,blank=True, null=True)
    company_desc = models.TextField(null=True, blank=True)
    company_logo = models.ImageField(upload_to='company/company_logos/', blank=True, null=True)
    stock_update_at = models.DateTimeField(null=True, blank=True)
    is_stock = models.BooleanField(default=False)
    pos_amount = models.IntegerField(default=0)

class EmailSettings(models.Model):
    emailsettings_id = models.BigAutoField(primary_key=True, editable=False)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    host = models.CharField(max_length=50, null=True, blank=True)
    port = models.CharField(max_length=50, null=True, blank=True)

class BillType(models.Model):
    bill_typeid = models.BigAutoField(primary_key=True, editable=False)
    bill_type = models.CharField(max_length=100, unique=True)

class Opening(models.Model):
    opening_id = models.BigAutoField(primary_key=True, editable=False)
    product = models.ForeignKey('Product', on_delete=models.RESTRICT,null=True, blank=True, related_name="openstockproductid")
    unit = models.ForeignKey('Unit', on_delete=models.SET_NULL, null=True,blank=True ,related_name='openunitid')
    convertion_value = models.IntegerField(default=1)
    batch_no = models.CharField(max_length=100)
    expire_date = models.DateField()
    total_qty = models.IntegerField()
    sales_amount = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    stock = models.ForeignKey('stock', on_delete=models.RESTRICT, null=True, blank=True, related_name="openstockstockid")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='openstockcreatedby')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='openstockeditedby')
    updated_at = models.DateTimeField(null=True, blank=True)  

class stock(models.Model):
    stock_id = models.BigAutoField(primary_key=True, editable=False)
    product = models.ForeignKey('Product', on_delete=models.RESTRICT,null=True, blank=True, related_name="stockproductid")
    unit = models.ForeignKey('Unit', on_delete=models.SET_NULL, null=True,blank=True ,related_name='stockunitid')
    batch_no = models.CharField(max_length=100)
    expire_date = models.DateField()
    sales_amount = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    unit_sales_amount = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    stock_qty = models.IntegerField()
    total_qty = models.IntegerField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Purchase(models.Model):
    purchase_id = models.BigAutoField(primary_key=True, editable=False)
    purchase_no = models.CharField(max_length=100,null=True, blank=True)
    purchase_date = models.DateTimeField(null=True, blank=True)
    sub_total = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    round_off = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    net_amount = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    paid_amount = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    bill_type = models.ForeignKey('BillType', on_delete=models.SET_NULL, null=True, blank=True, related_name="tpbilltypeid")
    notes = models.CharField(max_length=250, null=True, blank=True)
    is_locked = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tpcreatedby')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tpeditedby')
    updated_at = models.DateTimeField(null=True, blank=True)

class PurchaseDet(models.Model):
    purchasedet_id = models.BigAutoField(primary_key=True, editable=False)
    purchase = models.ForeignKey('Purchase', on_delete=models.RESTRICT, null=True, blank=True, related_name='tpdpurchaseid')
    product = models.ForeignKey('Product', on_delete=models.RESTRICT, related_name='tpditemid')
    unit = models.ForeignKey('Unit', on_delete=models.SET_NULL, null=True,blank=True ,related_name='tpdunitid')
    convertion_value = models.IntegerField(default=1)
    expire_date = models.DateField(null=True, blank=True)
    batch_no = models.CharField(max_length=100)
    qty = models.IntegerField()
    stock = models.ForeignKey('stock', on_delete=models.RESTRICT, null=True, blank=True, related_name="trpurchasedetstockid")
    mrp_amount = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    sales_amount = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    total_amount = models.DecimalField(default=0, decimal_places=2, max_digits=20)

class POS(models.Model):
    pos_id = models.BigAutoField(primary_key=True, editable=False)
    pos_no = models.CharField(max_length=100,null=True, blank=True)
    pos_date = models.DateTimeField(null=True, blank=True)
    sub_total = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    round_off = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    net_amount = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    paid_amount = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    bill_type = models.ForeignKey('BillType', on_delete=models.SET_NULL, null=True, blank=True, related_name="tposbilltypeid")
    notes = models.CharField(max_length=250, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tposcreatedby')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tposeditedby')
    updated_at = models.DateTimeField(null=True, blank=True)

class PosDet(models.Model):
    purchasedet_id = models.BigAutoField(primary_key=True, editable=False)
    pos = models.ForeignKey('POS', on_delete=models.RESTRICT, null=True, blank=True, related_name='tpdposid')
    category = models.ForeignKey('Category', on_delete=models.RESTRICT, related_name='tpdcategoryid')
    actual_wgt = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    avg_wgt = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    total_amount = models.DecimalField(default=0, decimal_places=2, max_digits=20)