from django.forms import ValidationError
from rest_framework import serializers
from flourishapi.models import *
from flourishapi.utils import *

# Bill no setting ::
class BillSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillnoSettings
        fields = ['billno_id','user', 'employee_prefix','employee_length','employee_live', 'bat_prefix',
                  'bat_length','bat_live', 'inv_prefix','inv_length','inv_live', 'pur_prefix',
                  'pur_length','pur_live']  
        
# Admin Settings ::
class AdminSettingsSerializer(serializers.ModelSerializer):
    stock_verified = serializers.SerializerMethodField()
    class Meta:
        model = AdminSettings
        fields = ['admin_settingsid','otp_length', 'otp_expiry_duration','user','is_maintenance_mode','company_name','company_contact_no',
                     'company_email', 'company_address', 'company_desc','company_logo','stock_update_at','is_stock','pos_amount','stock_verified']
    
    def get_stock_verified(self,obj):
        stock_update_at = obj.stock_update_at
        if stock_update_at is not None and stock_update_at.date() == date_only:
            return True
        return False 
        
# Email Settings ::
class EmailSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailSettings
        fields = ['emailsettings_id','email', 'password','port','host']