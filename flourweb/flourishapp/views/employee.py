import traceback
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import requests
import json
from rest_framework import status
from flourishapp.utils import *
url = settings.API_URL

# Employee Screen ::
def employee_screen(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        if not user_id or not token:
            return redirect('login')

        headers = {'Authorization': f'Bearer {token}'}
        generatecode = get_code(headers, 'EMP')
        usergroup = requests.get(f'{url}/common/getallusergroupapi/', headers=headers).json()
        context = {'usergroup': usergroup, 'generatecode': generatecode}

        if request.method == 'POST':
            data = {
                'employee_code': request.POST.get('txtEmployeeCode'),
                'first_name': request.POST.get('txtFirstName'),
                'last_name': request.POST.get('txtLastName'),
                'mobile_number': request.POST.get('txtMobileNumber'),
                'email': request.POST.get('txtEmail'),
                'address': request.POST.get('txtAddress'),
                'username': request.POST.get('txtUsername'),
                'usergroup': request.POST.get('ddlUsergroup'),
                'is_active': True,
                'password': request.POST.get('txtConfirmPassword'),
            }

            # IMAGES FILES FROM HTML
            files = {'employee_image': request.FILES.get('employeeImg')}
            if request.POST.get('hiddenEdit') == 'edit':
                edit_id = request.POST.get('hiddenEmployeeId')
                data.update({'updated_by': user_id, 'updated_at': dt})

                params = {'employee_id': edit_id}
                update_response = requests.put(f'{url}/masters/put-employee/', data=data, files=files, params=params, headers=headers)

                if update_response.status_code == status.HTTP_200_OK:
                    messages.success(request, CommonMessages.update('Employee'))
                    return redirect('employee-list')
                else:
                    error = update_response.json()
                    messages.error(request, CommonMessages.failed('Employee'))
                    context.update({'errors': error, 'data': data, 'edit': 'edit', 'employee_id': edit_id})
                    return render(request, 'mypanel/employee/employee.html', context)

            else:
                data.update({'created_by': user_id,'doj': formatted_date(request.POST.get('txtDOJ'))})
                post_response = requests.post(f'{url}/masters/post-employee/', files=files, data=data, headers=headers)

                if post_response.status_code == status.HTTP_201_CREATED:
                    messages.success(request, CommonMessages.create('Employee'))
                    return redirect('employee-list')
                else:
                    error = post_response.json()
                    messages.error(request, CommonMessages.create_failed('Employee'))
                    context.update({'errors': error, 'data': data})
                    return render(request, 'mypanel/employee/employee.html', context)

        else:
            employee_id = request.GET.get('employee_id')
            context = {
                "usergroup": usergroup,
               'generatecode': generatecode
            }
            if employee_id is not None:
                params = {"employee_id":employee_id}
                employee_data = requests.get('{url}/masters/edit-employee'.format(url=url),params=params,headers=headers).json()
                date_of_join = employee_data.get('doj')
                context.update({"employee_id": employee_id,"date_of_join":date_of_join})
            return render(request, 'mypanel/employee/employee.html', context)

    except Exception as e:
        return Response_errorhandler("employee_screen", request, e)

# Employee List Screen ::
def employee_list_screen(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        # Redirect to login if user is not authenticated
        if not user_id or not token:
            return redirect('login')
        
        return render(request,'mypanel/employee/employee_list.html')
    except Exception as e:
        return Response_errorhandler("employee_list_screen", request, e)
    

# Employee Datatable ::
def employee_dt(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        if not user_id or not token:
            return redirect('login')
        
        headers = {
            'Authorization': f'Bearer {token}'
        }
        data_tbl = dict(request.GET)
        params = {
            'user_id':user_id, 
            'data_table': json.dumps(data_tbl)
        }
        
        data = requests.get('{url}/masters/employee-dt-api'.format(url=url),params=params,headers=headers).json()
        return JsonResponse(data, safe=False)
    
    except Exception as e:
        return Response_errorhandler("employee_dt", request, e)

# Edit Employee ::
def edit_employee(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        if not user_id or not token:
            return redirect('login')
        
        headers = {
            'Authorization': f'Bearer {token}'
        }
        employee_id = request.GET.get('employee_id')
        params = {"employee_id":employee_id}

        data = requests.get('{url}/masters/edit-employee'.format(url=url),params=params,headers=headers).json()
        return JsonResponse(data, safe=False)
    
    except Exception as e:
        return Response_errorhandler("edit_employee", request, e)
    
# Delete Employee ::
def delete_employee(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        if not user_id or not token:
            return redirect('login')
        
        headers = {
            'Authorization': f'Bearer {token}'
        }
        employee_id = request.GET.get('employee_id')
        params = {"employee_id":employee_id}

        delete = requests.delete('{url}/masters/delete-employee/'.format(url=url),params=params,headers=headers)

        if delete.status_code == status.HTTP_200_OK:
            messages.success(request,CommonMessages.delete('Employee'))
            return redirect('employee-list')
        
        elif delete.status_code == status.HTTP_400_BAD_REQUEST :
            errors = delete.json()
            error = errors['message']
            messages.error(request,error)
            return redirect('employee-list')
        else:
            messages.error(request,CommonMessages.delete_failed('Employee'))
            return redirect('employee-list')
    
    except Exception as e:
        return Response_errorhandler("delete_employee", request, e)
    
# Update Employee status ::
def update_employee_status(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        if not user_id or not token:
            return redirect('login')
        
        headers = {
            'Authorization': f'Bearer {token}'
        }
        employee_id = request.GET.get("id")
        is_active = request.GET.get("sts")

        params = {"employee_id": employee_id, "is_active": is_active}

        updateFeatures = requests.put(
            "{url}/masters/update-employee-status/".format(url=url), params=params,headers=headers
        )

        if updateFeatures.status_code == status.HTTP_200_OK:
            messages.success(request, CommonMessages.update_status("Employee"))
            return redirect("employee-list")

        else:
            messages.error(request, CommonMessages.failed("Employee"))
            return redirect("employee-list")
    
    except Exception as e:
        return Response_errorhandler("update_employee_status", request, e)
    



    