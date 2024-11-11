from django.forms import ValidationError
from rest_framework import serializers
from flourishapi.models import *
from flourishapi.utils import *
from django.forms.models import model_to_dict
import datetime

# Get and Post Stock Opening Serializer
class StockOpeningSerializer(serializers.ModelSerializer):
    product_name = serializers.StringRelatedField(source="product.product_name")
    class Meta:
        model = Opening
        fields = '__all__'
    
class StockOpeningDatatableSerializer(serializers.ModelSerializer):
    product_name = serializers.StringRelatedField(source="product.product_name")
    expire_date = serializers.DateField(format="%d/%m/%Y")
    created_at = serializers.DateTimeField(format="%d/%m/%Y %I:%M %p")
    created_by = serializers.StringRelatedField(source="created_by.username")

    class Meta:
        model = Opening
        fields = ['opening_id','product','product_name','stock','batch_no','expire_date','sales_amount','total_qty','created_by','created_at','updated_by','updated_at']


class PostPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['purchase_id','purchase_no','purchase_date','sub_total','round_off','net_amount','paid_amount','bill_type','notes','created_by','created_at','updated_by','updated_at']

class GetTransPurchaseDetailsSerializers(serializers.ModelSerializer):
    purchaseDet = serializers.SerializerMethodField()

    class Meta:
        model = Purchase
        fields = ['purchase_id','purchase_no','purchase_date','sub_total','round_off','net_amount','paid_amount','bill_type','notes','purchaseDet']
        
    def get_purchaseDet(self,obj):
        list_ = []
        for data in obj.tpdpurchaseid.all():
            dict_1 = model_to_dict(data)
            dict_2 = {"product_name":data.product.product_name,"unit_name":data.unit.unit_name,"convertion_value":data.unit.convertion_value}
            dict_3 = {**dict_1,**dict_2}
            list_.append(dict_3)
        return list_

class PurchaseDetSerializer(serializers.ModelSerializer):
    product_name = serializers.StringRelatedField(source='product.product_name')
    unit_name = serializers.StringRelatedField(source='unit.unit_name')
    class Meta:
        model = PurchaseDet
        fields = ['purchase','product','product_name','expire_date','batch_no','qty','batch_no','unit_name','mrp_amount','sales_amount','total_amount']


class GetPurchaseSerializer(serializers.ModelSerializer):
    bill_type = serializers.StringRelatedField(source='bill_type.bill_type')
    purchase_date = serializers.DateTimeField(format="%d/%m/%Y %I:%M %p")
    # isalter = serializers.SerializerMethodField()
    purchaseDet = serializers.SerializerMethodField()
    class Meta:
        model = Purchase
        fields = ['purchase_id','purchase_no','purchase_date','net_amount','bill_type','purchaseDet']
    
    def get_isalter(self,obj):
        result = True
        det_detsil = obj.tpdpurchaseid.all()
        for det in det_detsil:
            if det.stock.stock_qty < det.qty:
                result = False   
        return result
    
    def get_purchaseDet(self,obj):
        list_ = []
        for data in obj.tpdpurchaseid.all():
            dict_1 = model_to_dict(data)
            dict_2 = {"product_name":data.product.product_name,"qty":data.qty}
            dict_3 = {**dict_1,**dict_2}
            list_.append(dict_3)
        return list_
        

class StockDtSerializer(serializers.ModelSerializer):
    product_name = serializers.StringRelatedField(source='product.product_name')
    unit_name = serializers.StringRelatedField(source='unit.unit_name')
    created_at = serializers.DateTimeField(format="%d/%m/%Y %I:%M %p")
    class Meta:
        model = stock
        fields = ['stock_id','batch_no','expire_date','batch_no','sales_amount','unit_sales_amount','stock_qty','product_name','unit_name','total_qty','product','unit','created_at']

class PostPosSerializer(serializers.ModelSerializer):
    class Meta:
        model = POS
        fields = ['pos_id','pos_no','pos_date','sub_total','round_off','net_amount','paid_amount','bill_type','notes','created_by','created_at','updated_by','updated_at']


class PosDetSerializer(serializers.ModelSerializer):
    category_name = serializers.StringRelatedField(source='category.category_name')
    class Meta:
        model = PosDet
        fields = ['purchasedet_id','pos','category','category_name','actual_wgt','avg_wgt','total_amount']

class GetPosDetailsSerializers(serializers.ModelSerializer):
    posDetails = serializers.SerializerMethodField()

    class Meta:
        model = POS
        fields = ['pos_id','pos_no','pos_date','sub_total','round_off','net_amount','paid_amount','bill_type','notes','posDetails']
        
    def get_posDetails(self,obj):
        list_ = []
        for data in obj.tpdposid.all():
            dict_1 = model_to_dict(data)
            dict_2 = {"category_name":data.category.category_name,"actual_wgt":data.actual_wgt,"avg_wgt":data.avg_wgt,"total_amount":data.total_amount}
            dict_3 = {**dict_1,**dict_2}
            list_.append(dict_3)
        return list_
    
class PosDtSerializer(serializers.ModelSerializer):
    bill_type = serializers.StringRelatedField(source='bill_type.bill_type')
    pos_date = serializers.DateTimeField(format="%d/%m/%Y %I:%M %p")
    class Meta:
        model = POS
        fields = ['pos_id','pos_no','pos_date','sub_total','round_off','net_amount','paid_amount','bill_type','notes']