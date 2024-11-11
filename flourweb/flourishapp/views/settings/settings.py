import traceback
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import requests
import json
from rest_framework import status
url = settings.API_URL
from flourishapp.utils import *

# Settings Screen ::
def Settings_screen(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        if not user_id or not token:
            return redirect('login')
        
        headers = {
            'Authorization': f'Bearer {token}'
        }
        get_admin_settings = requests.get('{url}/settings/get-admin-settings/'.format(url=url),headers=headers).json()
        get_email_settings = requests.get('{url}/settings/get-email-settings/'.format(url=url),headers=headers).json()

        context={'get_admin_settings':get_admin_settings, 'get_email_settings': get_email_settings}
        return render(request,'mypanel/settings/settings.html',context=context)
    
    except Exception as e:
        return Response_errorhandler("Settings_screen", request, e)

# Billno Settings Screen ::
def billno_Settings_screen(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        if not user_id or not token:
            return redirect('login')
        
        headers = {
            'Authorization': f'Bearer {token}'
        }
        get_bill_settings = requests.get('{url}/settings/get-billno-settings/'.format(url=url),headers=headers).json()
        if request.method == 'POST':
                
            data = {
                'user': user_id,
                'employee_prefix': request.POST.get('txtEmpPrefix'),
                'employee_length': request.POST.get('txtEmpLength'),
                'employee_live': request.POST.get('txtEmpLive'),
                'bat_prefix': request.POST.get('txtBatPrefix'),
                'bat_length': request.POST.get('txtBatLength'),
                'bat_live': request.POST.get('txtBatLive'),
                'inv_prefix': request.POST.get('txtInvPrefix'),
                'inv_length': request.POST.get('txtInvLength'),
                'inv_live': request.POST.get('txtInvLive'),
                'pur_prefix': request.POST.get('txtPurPrefix'),
                'pur_length': request.POST.get('txtPurLength'),
                'pur_live': request.POST.get('txtPurLive'),
                
            }
            
            datalist = requests.post('{url}/settings/post-billno-settings/'.format(url=url),headers=headers,data=data)
            if datalist.status_code == status.HTTP_201_CREATED:
                messages.success(request,CommonMessages.create('Billnosetting'))
                return redirect('billno-settings')
            if datalist.status_code == status.HTTP_200_OK:
                messages.success(request,CommonMessages.update('Billnosetting'))
                return redirect('billno-settings')
            else:
                messages.error(
                    request,CommonMessages.failed('Billnosetting'))
                return redirect('billno-settings')

        context={'get_bill_settings':get_bill_settings}
        return render(request,'mypanel/settings/billnosettings.html',context=context)
    
    except Exception as e:
        return Response_errorhandler("billno_Settings_screen", request, e)
    
def update_admin_setting(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        if not user_id or not token:
            return redirect('login')
        
        headers = {
            'Authorization': f'Bearer {token}'
        }
        
        if request.method == 'POST':
            
            data = {
                'otp_length': request.POST.get('txtOtpLength'),
                'otp_expiry_duration': request.POST.get('txtOtpExpired'),
                'is_maintenance_mode': True,
                'company_name': request.POST.get('txtCompanyName'),
                'company_contact_no': request.POST.get('txtContactNo'),
                'company_email': request.POST.get('txtCompanyEmail'),
                'company_address': request.POST.get('txtCompanyAddress'),
                'company_desc': request.POST.get('txtCompanyDesc'),
                'pos_amount': request.POST.get('txtPOSAmount'),
                'user':user_id
            }
            files = {
                'company_logo':request.FILES.get('companyImg')
            }
         
            datalist = requests.post('{url}/settings/post-admin-settings/'.format(url=url),files=files,headers=headers,data=data)
            if datalist.status_code == status.HTTP_201_CREATED:
                messages.success(
                    request,CommonMessages.create('Admin setting'))
                return redirect('settings')
            if datalist.status_code == status.HTTP_200_OK:
                messages.success(
                    request,CommonMessages.update('Admin setting'))
                return redirect('settings')
            else:
                messages.error(
                    request,CommonMessages.update('Admin setting'))
                return redirect('settings')
        
    except Exception as e:
        return Response_errorhandler("update_admin_setting", request, e)
        
# Update Email Settings ::
def update_email_setting(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        if not user_id or not token:
            return redirect('login')
        
        headers = {
            'Authorization': f'Bearer {token}'
        }
        
        if request.method == 'POST':
            data = {
                'email': request.POST.get('txtEmailAddress'),
                'password': request.POST.get('txtPassword'),
                'host': request.POST.get('txtHostName'),
                'port': request.POST.get('txtPortNumber'),
                }
 
            datalist = requests.post('{url}/settings/post-email-settings/'.format(url=url),headers=headers,data=data)
            if datalist.status_code == status.HTTP_201_CREATED:
                messages.success(
                    request,CommonMessages.create('Email setting'))
                return redirect('settings')
            if datalist.status_code == status.HTTP_200_OK:
                messages.success(
                    request,CommonMessages.update('Email setting'))
                return redirect('settings')
            
            else:
                error = datalist.json()
                messages.error(
                    request,CommonMessages.failed('Email setting'))
                return redirect('settings')
    
    except Exception as e:
        return Response_errorhandler("update_email_setting", request, e)
    

def log_list_screen(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        # Redirect to login if user is not authenticated
        if not user_id or not token:
            return redirect('login')
        
        return render(request,'mypanel/settings/log.html')
        
    except Exception as e:
        return Response_errorhandler("log_list_screen", request, e)


def log_screen(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        if not user_id or not token:
            return redirect('login')
        headers = {
            'Authorization': f'Bearer {token}'
        }
        data_tbl = dict(request.GET)
        start_date = request.GET.get('start_date') 
        end_date = request.GET.get('end_date')
        type = request.GET.get('type')
 
        params = {
            'user_id':user_id, 
            'start_date':start_date,
            'end_date':end_date,
            'type':type, 
            'data_table': json.dumps(data_tbl)
        }
        data = requests.get('{url}/common/log-dt'.format(url=url),params=params,headers=headers).json()
        return JsonResponse(data, safe=False)
    
    except Exception as e:
        return Response_errorhandler("log_screen", request, e)