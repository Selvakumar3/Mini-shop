from rest_framework.response import Response
from rest_framework import status
from flourishapi.models import *
import traceback
import uuid
import re
from django.db.models import Max
import requests
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import socket
from datetime import datetime, timedelta, timezone
from django.utils.timezone import localtime
# from flourishapi.bulk_creations import *

# Get default time :
date_time = localtime(datetime.now(timezone.utc))
date_only = localtime(datetime.now(timezone.utc)).date()

# Save error in table :
def Log(transaction_name, msg, Ip, Mode=None, userid=None,log_type=None):
    HOSTNAME = socket.gethostname()
    Logs.objects.create(
        transaction_name=transaction_name, mode=Mode, log_message=str(msg),
        user_id=userid,system_name=HOSTNAME, Ip_address=Ip,log_date=date_time,log_type=log_type)
    
# error response for api
Type = 'API'
class error_response:
    
    @staticmethod
    def serializer_error(className, request, serializer, user_id=None):
        errors = serializer.errors
        if serializer.errors.get('non_field_errors', ''):
            errors = serializer.errors['non_field_errors'][0]
        elif serializer.errors.get('email', ''):
            errors = serializer.errors['email'][0]

        Ip = request.META['REMOTE_ADDR']
        msg = {'status': status.HTTP_400_BAD_REQUEST,'message': errors}
        Log(className, msg, Ip, request.method, user_id,Type)
        return Response(msg, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def exception_error(className, request, e, user_id=None):
        log_msg={'error':str(e),'traceback':traceback.format_exc()}
        Ip = request.META['REMOTE_ADDR']
        mode = None
        Log(className, log_msg, Ip, request.method, user_id,Type)
        error = {'status':status.HTTP_400_BAD_REQUEST, 'message' : 'Something went wrong!'}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def restricted_error(className, request, errorName, user_id=None):
        Ip = request.META['REMOTE_ADDR']
        error_message = f'{errorName} is being referenced with another instance'
        error_data = {'status': status.HTTP_409_CONFLICT, 'message': error_message}
        Log(className, request.method, error_data, Ip, user_id,Type)

    @staticmethod
    def validation_error(msg, user_status):
        error_data = {'status':user_status, 'message': msg}
        return Response(error_data, status=status.HTTP_400_BAD_REQUEST)
    

# Django ORM methods to querys ::
def getFirstObject(model):
    return model.objects.first()

def getLastObject(model):
    return model.objects.last()

def getAllObject(model):
    return model.objects.all()

def getObject(model, filter_params={}):
    return model.objects.get(**filter_params)

def getAllObjectWithFilter(model, filter_params={}):
    return model.objects.filter(**filter_params)

def getAllObjectWithPrefetchFilter(model,  prefetch_value, filter_params={}):
    return model.objects.prefetch_related(prefetch_value).filter(**filter_params)

def getObjectWithExcludeFilter(model, filter_params={}):
    return model.objects.exclude(**filter_params)

# Set default values for conditions :

class VelanEmailType:
    PASSWORD_RESET_LINK = 1

class VelanEmailSettingsType:
    NOREPLY = 1
    PARTNER = 2


# Set messages for error ::

class CommonApiMessages:

    @staticmethod

    def create(msg):
        message = {'message':f"{msg} created successfully"}
        return message
    
    def update(msg):
        message = {'message':f"{msg} updated successfully"}
        return message
    
    def failed(msg):
        message = {'message':f"Failed to update {msg}"}
        return message
    
    def delete (msg):
        message = {'message':f"{msg} deleted successfully"}
        return message
    
    def restrict_delete (msg):
        message = {'message':f"{msg} is being referenced with another instance"}
        return message
    
    def update_status (msg):
        message = {'message':f"{msg} status updated successfully"}
        return message
    
    def exists (msg):
        message = f"{msg} already exists"
        return message
    
    def existsContent(msg):
        message = f'This {msg} type ID has already been assigned to content.'
        return message
    
    def does_not_exists(msg):
        message = f'{msg} ID does not exists.'
        return message

#-------------------------------------------  Auto Generate code--------------------------------------

def code_generating(code_type):
    billno = BillnoSettings.objects.first()
    Prefix = ''
    cod_Length = 0
    cod_Live = 0
    
    if code_type == 'EMP':
        Prefix = billno.employee_prefix
        cod_Length = billno.employee_length
        cod_Live = billno.employee_live
        
    if code_type == 'BAT':
        Prefix = billno.bat_prefix
        cod_Length = billno.bat_length
        cod_Live = billno.bat_live
        
    if code_type == 'INV':
        Prefix = billno.inv_prefix
        cod_Length = billno.inv_length
        cod_Live = billno.inv_live
        
    if code_type == 'PUR':
        Prefix = billno.pur_prefix
        cod_Length = billno.pur_length
        cod_Live = billno.pur_live
        
    if Prefix == None:
        Prefix = ''

    if cod_Live == 0:
        cod_Live = 1
        cod_id_digits = str(cod_Live).zfill(cod_Length)
        cod_number = Prefix + cod_id_digits
    else:
        cod_id_digits = str(cod_Live + 1).zfill(cod_Length)
        cod_number = Prefix + cod_id_digits
    return cod_number


def code_update(code_type):
    billno = BillnoSettings.objects.first()
    
    if  code_type == 'EMP':  
        billno.employee_live = billno.employee_live + 1
        
    if  code_type == 'BAT':
        billno.bat_live = billno.bat_live + 1
        
    if  code_type == 'INV':  
        billno.inv_live = billno.inv_live + 1
        
    if  code_type == 'PUR':  
        billno.pur_live = billno.pur_live + 1
        
    billno.save() 