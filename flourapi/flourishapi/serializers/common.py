from rest_framework import serializers
from flourishapi.models import *
from flourishapi.utils import *
from django.forms import ValidationError

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logs
        fields = '__all__'

# MENU SERIALIZERS ::
class menuDetailsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['menu_id','menu_name','url','file_name','icon_path','parent_id','row_index','is_module','is_visible',
                  'description','is_administrator']
        
# Usergroup Serializers ::
class PostUserGroupMenuSerializers(serializers.ModelSerializer):
    usergroup_name = serializers.CharField()
    class Meta:
        model = UserGroup
        fields = ['usergroup_id', 'usergroup_name','created_by','created_date','updated_by','updated_at']

    def validate_usergroup_name(self, data):
        usergroup_id = self.context.get("usergroup_id")
        qs =  getAllObjectWithFilter(UserGroup,{'usergroup_name':data})
        if usergroup_id:
            qs = qs.exclude(usergroup_id=usergroup_id)
        if qs.exists():
            raise serializers.ValidationError(CommonApiMessages.exists("User group"))
        return data
    
class UserMenuSerializers(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['menu_id', 'menu_name', 'is_module', 'parent_id','row_index']


class UserGroupListMenuSerializers(serializers.ModelSerializer):
    Menu = serializers.SerializerMethodField()
   
    class Meta:
        model = UserGroup
        fields = ['usergroup_id', 'usergroup_name','Menu']

    def get_Menu(self, args):
        from django.db.models import Q

        menu_id = getAllObjectWithFilter(UserGroupMenu,{'usergroup':args.usergroup_id}).values_list('menu', flat=True)
        menu = Menu.objects.filter(menu_id__in=menu_id).filter(Q(is_module=0) | Q(Q(is_module=1))).values_list('menu_id', flat=True)
        return menu
    
class GetLogReportsSerializer(serializers.ModelSerializer):
    log_date = serializers.DateTimeField(format="%d/%m/%Y %I:%M %p")
    class Meta:
        model = Logs
        fields = ["log_id","transaction_name","mode","Ip_address","system_name","log_date","log_type","log_message"]
