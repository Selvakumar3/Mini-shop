from django.forms import ValidationError
from rest_framework import serializers
from flourishapi.models import *
from flourishapi.utils import *

# GET ALL Category SERIALIZERS
class GetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "categoryid",
            "category_name",
            "category_desc",
            "category_image",
            "is_active"
        ]

# POST Category SERIALIZERS
class PostCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField()

    class Meta:
        model = Category
        fields = GetCategorySerializer.Meta.fields + [
            "created_by",
            "created_at",
            "updated_by",
            "updated_at",
        ]

    def validate_category_name(self, data):
        category_id = self.context.get("category_id")
        qs =  getAllObjectWithFilter(Category,{'category_name':data})
        if category_id:
            qs = qs.exclude(categoryid=category_id)
        if qs.exists():
            raise serializers.ValidationError(CommonApiMessages.exists("Category"))
        return data


# GET ALL Brand SERIALIZERS
class GetBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            "brand_id",
            "brand_name",
            "brand_image",
            "category",
            "is_active",
        ]
 
class GetBrandDtSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    class Meta:
        model = Brand
        fields = [
            "brand_id",
            "brand_name",
            "brand_image",
            "category",
            "is_active",
            "category_name"
        ]
    def get_category_name(self, obj):
        return obj.category.category_name if obj.category else ""

# POST Brand SERIALIZERS
class PostBrandSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField()

    class Meta:
        model = Brand
        fields = GetBrandSerializer.Meta.fields + [
            "created_by",
            "created_at",
            "updated_by",
            "updated_at",
        ]

    def validate_brand_name(self, data):
        brand_id = self.context.get("brand_id")
        qs =  getAllObjectWithFilter(Brand,{'brand_name':data})
        if brand_id:
            qs = qs.exclude(brand_id=brand_id)
        if qs.exists():
            raise serializers.ValidationError(CommonApiMessages.exists("Brand"))
        return data
    
# GET ALL Unit SERIALIZERS
class GetUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = [
            "unit_id",
            "unit_name",
            "convertion_value"
           
        ]

# POST Unit SERIALIZERS
class PostUnitSerializer(serializers.ModelSerializer):
    unit_name = serializers.CharField()

    class Meta:
        model = Unit
        fields = GetUnitSerializer.Meta.fields + [
            "created_by",
            "created_at",
            "updated_by",
            "updated_at",
        ]

    def validate_unit_name(self, data):
        unit_id = self.context.get("unit_id")
        qs =  getAllObjectWithFilter(Unit,{'unit_name':data})
        if unit_id:
            qs = qs.exclude(unit_id=unit_id)
        if qs.exists():
            raise serializers.ValidationError(CommonApiMessages.exists("Unit"))
        return data
    
# GET ALL Product SERIALIZERS
class GetProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "product_id",
            "product_name",
            "category",
            "brand",
            "unit",
            "product_image",
            "mrp",
            "customer_price",
            "desc",
            "is_active",
           
        ]

# POST Product SERIALIZERS
class PostProductSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField()

    class Meta:
        model = Product
        fields = GetProductSerializer.Meta.fields + [
            "created_by",
            "created_at",
            "updated_by",
            "updated_at",
        ]

    def validate_product_name(self, data):
        product_id = self.context.get("product_id")
        qs =  getAllObjectWithFilter(Product,{'product_name':data})
        if product_id:
            qs = qs.exclude(product_id=product_id)
        if qs.exists():
            raise serializers.ValidationError(CommonApiMessages.exists("Product"))
        return data
    
class GetProductDtSerializer(serializers.ModelSerializer):
    brand_name = serializers.SerializerMethodField()
    unit_name = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = [
            "product_id",
            "product_name",
            "category",
            "brand",
            "unit",
            "product_image",
            "mrp",
            "customer_price",
            "desc",
            "sales_count",
            "is_active",
            "brand_name",
            "unit_name",
        ]
    def get_brand_name(self, obj):
        return obj.brand.brand_name if obj.brand else ""
    
    def get_unit_name(self, obj):
        return obj.unit.unit_name if obj.unit else ""
    
# GET Dt Employee SERIALIZERS
class GetEmployeeDtSerializer(serializers.ModelSerializer):
    doj = serializers.DateTimeField(format="%d/%m/%Y %I:%M %p")
    class Meta:
        model = Employee
        fields = [
            "employee_id",
            "employee_no",
            "first_name",
            "last_name",
            "doj",
            "mobile_number",
            "email",
            "employee_image",
            "address",
            "username",
            "usergroup",
            "is_active",
            "emp_user",
        ]

# GET ALL Employee SERIALIZERS
class GetEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            "employee_id",
            "employee_no",
            "first_name",
            "last_name",
            "doj",
            "mobile_number",
            "email",
            "employee_image",
            "address",
            "username",
            "usergroup",
            "is_active",
            "emp_user",
        ]

# POST Employee SERIALIZERS
class PostEmployeeSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = Employee
        fields = GetEmployeeSerializer.Meta.fields + [
            "created_by",
            "created_at",
            "updated_by",
            "updated_at",
        ]

    def validate_username(self, data):
        employee_id = self.context.get("employee_id")
        qs =  getAllObjectWithFilter(Employee,{'username':data})
        if employee_id:
            qs = qs.exclude(employee_id=employee_id)
        if qs.exists():
            raise serializers.ValidationError(CommonApiMessages.exists("Employee"))
        return data