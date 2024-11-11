import traceback
from datetime import datetime, timezone
import requests
from django.utils.timezone import localtime
from django.shortcuts import render,redirect
from django.conf import settings
from django.http import JsonResponse
from django.contrib import messages
url = settings.API_URL

dt = datetime.now(timezone.utc)
dt = localtime(dt)

from datetime import datetime

def formatted_date(date):
    format = "%d/%m/%Y"  # Change to match DD/MM/YYYY
    return datetime.strptime(date, format).date()


def generate_batch_no(prefix):
    # Get the current date
    current_date = datetime.now()
    month = current_date.strftime("%b").upper()
    day = current_date.day
    variable = f"{prefix}{month}{day:02d}"
    return variable


def Response_errorhandler(Transactionname, request, error):
    
    import socket
    user_id = request.session['user_id']
    Ip = request.META['REMOTE_ADDR']
    HOSTNAME = socket.gethostname()
    dt = datetime.now(timezone.utc)
    dt = localtime(dt)

    msg={'error':str(error),'traceback':traceback.format_exc()}
    data = {"transaction_name": Transactionname,
            "log_date": dt, "log_message": str(msg), "Ip_address": Ip, 
            'user': user_id, 'system_name': HOSTNAME, 'mode':request.method,"log_type":"Web"}
    
    res_api = requests.post('{url}/common/log/'.format(url=url), data=data)
    return render(request,'500.html')

    
def check_url_permission(url_name=None):
    
    try:
        def permission(view_func):
            def wrapper(request, *args, **kwargs):
                # Check if Token, userId exist in the session
                token = request.session.get('Token')
                user_id = request.session.get('UserId')
                if not (token and user_id):
                    return redirect('login')

                # Get the URL from the parameter or the previous path URL
                url_path = url_name or request.path

                headers = {'Authorization': f'Token {token}'}
                params = {'url_path': url_path, 'user_id':user_id}
                url_permission = requests.get('{url}/common/check-url-permission/'.format(url=url), params=params, headers=headers).json()
                print('*******URL Permission*******',url_permission)
                if url_permission.get('isPermission') == False:
                    messages.error(request, 'You dont have permission to access')
                    return redirect('dashboard')
                if url_permission.get('parentId'):
                    request.session['parentId'] = url_permission.get('parentId')
                # Call the actual view function and return the response
                return view_func(request, *args, **kwargs)

            return wrapper
        return permission
    except Exception as e:
        import traceback
        print(traceback.format_exc(), str(e), '==============error')


class CommonMessages:

    @staticmethod

    def create(msg):
        return  f"{msg} created successfully"
    
    def update(msg):
        return f"{msg} updated successfully"
    
    def failed(msg):
        return f"Failed to update {msg}"
    
    def create_failed(msg):
        return f"Failed to create {msg}"
    
    def delete (msg):
        return f"{msg} deleted successfully"
    
    def delete_failed (msg):
        return f"Failed to delete {msg}"
    
    def restrict_delete (msg):
        return f"{msg} is being referenced with another instance"
    
    def update_status (msg):
        return f"{msg} status updated successfully"
    
    
# Common Functions ::
def getcategories(headers=None):
    categories = requests.get(
        "{url}/masters/get-all-category/".format(url=url), headers=headers
    ).json()
    return categories

def getbrand(headers=None):
    brand = requests.get(
        "{url}/masters/get-all-brand/".format(url=url), headers=headers
    ).json()
    return brand

def getunit(headers=None):
    unit = requests.get(
        "{url}/masters/get-all-unit/".format(url=url), headers=headers
    ).json()
    return unit

def getproduct(headers=None):
    product = requests.get(
        "{url}/masters/get-all-product/".format(url=url), headers=headers
    ).json()
    return product

def get_code(headers=None,code=None):
    code = requests.get(
        "{url}/common/generatecode/".format(url=url), headers=headers,params={'codetype':code}
    ).json()
    return code

def get_billtype(headers=None,code=None):
    data = requests.get(
        "{url}/common/get-bill-type/".format(url=url), headers=headers
    ).json()
    return data

def get_admin_settings(headers=None,):
    data = requests.get(
        "{url}/settings/get-admin-settings/".format(url=url), headers=headers
    ).json()
    return data

