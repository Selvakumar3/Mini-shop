from rest_framework import serializers
from django.contrib.auth import authenticate
from flourishapi.models import *
from django.conf import settings
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ValidationError

# -------forgot password----------
from django.http.response import HttpResponsePermanentRedirect
from django.utils.encoding import  force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

FRONTEND_URL = settings.FRONTEND_URL

# Login Serializers 
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        max_length=125,
        write_only=True
    )

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        try:
            user = User.objects.get(username=username)  # Use 'username' if that's the field name
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Enter valid username!')

        if user.check_password(password):
            #authenticate userdetails 
            user = authenticate(request=self.context.get('request'), username=username, password=password)
        else:
            raise serializers.ValidationError('Password is incorrect!.')
        
        data['user'] = user
        return data


# RESET PASSWORD VALIDATIONS::
class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    class Meta:
        fields = ['email']

# Redirect Password 
class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [FRONTEND_URL,'http','https']      

# Create New Password After Send Email ::
class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        password = attrs.get('password')
        token = attrs.get('token')
        uidb64 = attrs.get('uidb64')

        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise ValidationError( 'Password reset Url expired')
        user.set_password(password)
        user.save()
        return user
        # return CustomRedirect(f"{FRONTEND_url}{redirect_url}?emailid={email}&token_valid=False")

class GetUserProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()
    profile_verified = serializers.SerializerMethodField()
  
    class Meta:
        model = User
        fields = ['id','username','display_name','email','mobile_number','profile_image','display_name','profile_verified']
        
    def get_profile_image(self, obj):
        if obj.profile_image and obj.profile_image != '':
            request = self.context.get('request')
            return request.build_absolute_uri(obj.profile_image.url)
        return '/static/images/spear-logo.jpg'
    
    def get_profile_verified(self, obj):
        return bool(obj.display_name) and bool(obj.email) and bool(obj.profile_image)
    
class UserProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()
   
    class Meta:
        model = User
        fields = ['id','username','display_name','email','mobile_number','profile_image','display_name']
        
    def get_profile_image(self, obj):
        if obj.profile_image == '':
            result = None
        else:
            request = self.context.get('request')
            result = request.build_absolute_uri(obj.profile_image.url)
        return result
    
class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','display_name','email','mobile_number','profile_image']


# USER PROFILE SERIALIZERS ::
class UserProfileImageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'profile_image', 'display_name','username','email']


# GET USER PROFILE SERIALIZERS ::
class GetUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','display_name','email','mobile_number','profile_image','is_super_admin','is_admin','is_active']

# POSt USER  SERIALIZERS ::
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'display_name', 'usergroup','mobile_number','is_admin','is_active','password']
        
    def validate_username(self, data):
        if User.objects.filter(username=data).exists():
            raise serializers.ValidationError("User Name Already Exists")
        else:
            return data
       
    def validate_mobile_number(self, data):
        mobile_number = data
        mobile_number_queryset = User.objects.filter(mobile_number__iexact=mobile_number)
        if len(mobile_number) != 10:
            raise serializers.ValidationError("Mobile Number Should be 10 Digits")
        if mobile_number_queryset.exists():
            raise serializers.ValidationError("Mobile Number Already Exists")  
        return data