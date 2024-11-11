import traceback
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import requests
from rest_framework import status
from flourishapp.utils import *
from django.urls import reverse
import json


url = settings.API_URL
mode = 'edit'

# Login functions ::
def Login(request):
    try:
        if request.method == 'POST':
            data = {
                'username': request.POST.get('txtUserName'),
                'password': request.POST.get('txtPassword')
            }
            login_data = requests.post('{url}/user/login/'.format(url=url),data=data)            
            if login_data.status_code == status.HTTP_202_ACCEPTED:
                user_data = login_data.json()
                request.session['token']=user_data.get('token')
                request.session['refresh_token']=user_data.get('refresh_token')
                request.session['user_id']=user_data.get('user_id')
                request.session['is_admin']=user_data.get('is_admin')
                request.session['is_super_admin']=user_data.get('is_super_admin')
                request.session['username']= user_data.get('username')
                request.session['display_name']= user_data.get('display_name')
                request.session['email'] = user_data.get('email')
                request.session['profile_image'] = user_data.get('profile_image')
                messages.success(request, 'Logged in Successfully')
                return redirect('dashboard')
            else:
                error = login_data.json()
                error_message = error.get('message')               
                context = {'data':data}
                messages.error(request,error_message)
                return render(request, 'login.html', context=context)
        else:
            return render(request,'login.html')
    except Exception as e:
        return Response_errorhandler("login", request, e)
    

def Logout(request):
    try:
        token = request.session.get('token')
        refresh_token = request.session.get('refresh_token')

        headers = {
            'Authorization': f'Bearer {token}'
        }
        logout_response = requests.post(
            f'{url}/user/v1/auth/logout/',  # Correctly formatted URL
            json={'refresh_token': refresh_token},  # Directly pass json
            headers=headers
        )

        if logout_response.status_code == status.HTTP_205_RESET_CONTENT:
            # Clear session data
            request.session.flush()
            messages.success(request, "Logged out successfully!")
            return redirect('login')
        else:
            messages.error(request, "Failed to log out!")
            return redirect('dashboard')
        
    except Exception as e:
        return Response_errorhandler("Logout", request, e)


# User forget password request screen ::
def forget_password_screen(request):
    """
    Summary or Description of the Function:
        *  User Forget Password data and the bind data to input field.
    Method: ,'POST'
    """
    try:
        if request.method == "POST":
            data = {
                "email": request.POST.get("txtEmail")
            }
            post = requests.post(f'{url}/user/user-forgot-password/',data=data)
      
            if post.status_code == status.HTTP_201_CREATED:
                messages.success(request, "Reset link sent your email successfully")
                return redirect('login')
            
            elif post.status_code == status.HTTP_404_NOT_FOUND:
                messages.error(request, "Email is invalid")
                return redirect('login')
            else:
                messages.error(request,"Email sent failed.")
                return redirect('login')
        else:
            return render(request,'forget_password.html')

    except Exception as e:
        return Response_errorhandler("forget_password_screen", request, e)

# User reset password functins ::
def reset_password(request):
    """
    Summary or Description of the Function:
        *  User Reset Password data and Send Email TO link with Expired Time  to input field.
    Method: ,'POST'
    """
    try:
        email = request.GET.get("emailid")
        context = {"email": email}

        if request.method == "POST":
            temptoken = request.session["temptoken"]
            uidb64 = request.session["uidb64"]

            data = {
                "password": request.POST.get("txtPassword"),
                "token": temptoken,
                "uidb64": uidb64,
            }
            new_password = requests.put(
                "{url}/user/user-forgot-password/".format(url=url),
                data=data
            )
            if new_password.status_code == status.HTTP_200_OK:
                msg = new_password.json()
                messages.success(request, msg['message'])
                return redirect('/')
            else:
                error = new_password.json()
                reset_url = reverse("reset-password")
                reset_url += f"?emailid={request.POST.get('hdEmail')}&token_valid=False"
                return redirect(reset_url)
        else:

            # After Reset Password Link Expired Valid False :;
            if request.GET.get('token_valid') == 'False':
                messages.error(request, 'Sorry,Link has expired please request a new one')
                return render(request, "reset_password.html", context=context)
            
            elif request.GET.get('token_valid') == 'True':
                request.session['temptoken'] = request.GET.get('token')
                request.session['uidb64'] = request.GET.get('uidb64')
                return render(request, "reset_password.html", context=context)
            else:
                return render(request, "reset_password.html", context=context)
    except Exception as e:
        return Response_errorhandler("forget_password_screen", request, e)

# USERGROUP LIST functions ::
def usergroup_screen(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        if not user_id or not token:
            return redirect('login')

        return render(request,'mypanel/user/usergroup.html')
    except Exception as e:  
        return Response_errorhandler("usergroup_screen", request, e)
 
# GET USERGROUP MENU DATA:
def GetUserGroupMenu(request): 
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        if not user_id or not token:
            return redirect('login')
        
        headers = {
            'Authorization': f'Bearer {token}'
        }
        params={'user_id':user_id}

        data = requests.get('{url}/common/getusergroupmenu/'.format(url=url),params=params, headers=headers).json()
        return JsonResponse(data,safe=False)
    
    except Exception as e:  
        return Response_errorhandler("GetUserGroupMenu", request, e)

# POST AND UPDATE Usergroup FUNCTION::
def PostUserGroup(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        if not user_id or not token:
            return redirect('login')
        headers = {
            'Authorization': f'Bearer {token}'
        }
        params={'user_id':user_id}

        usergrouplist = requests.get('{url}/common/getusergrouplist/'.format(url=url),headers=headers,params=params).json()
        context={'usergrouplist':usergrouplist}
       
        if request.method == 'POST':
                
            usergroup_name = request.POST['txtusergroupName']
            usergroup_id = request.POST.get('txtUpdateId')
            edit = request.POST.get('txtEdit')
            menu_id = request.POST.get('menuIdDet') 
            
            if edit == 'edit' :
                data = {'usergroup_name':usergroup_name,
                    'updated_by':user_id,
                    'updated_at':dt,
                    'menuIdDet':menu_id
                    }
                params={'usergroup_id':usergroup_id,'user_id':user_id}
                usergroup =requests.put('{url}/common/updateusergroupmenu/'.format(url=url),headers=headers,data=data,params=params)

                if usergroup.status_code == status.HTTP_200_OK:
                    messages.success(request,'Usergroup updated successfully')
                    return redirect('usergroup')
                else:
                    error = usergroup.json()
                    messages.error(request,'Usergroup failed to update')
                    context={'errors':error,'usergrouplist':usergrouplist,'data':data,'edit':'edit','usergroup_id':usergroup_id,'bind':'bind'}
                    return render(request,'mypanel/user/usergroup.html',context=context)   
                
            else:
                    data={'usergroup_name':usergroup_name,
                        'created_by':user_id,
                        'menuIdDet':menu_id}
                    
                    params={'user_id':user_id}
                    usergroup =requests.post('{url}/common/postusergroupmenu/'.format(url=url),headers=headers,data=data,params=params)

                    if usergroup.status_code == status.HTTP_201_CREATED:
                        messages.success(request,'Usergroup created successfully')
                        return redirect('usergroup')
                    else:
                        error = usergroup.json()
                        messages.error(request,'Usergroup created failed')
                        context={'errors':error,'usergrouplist':usergrouplist,'data':data,'bind':'bind'}
                        return render(request,'mypanel/user/usergroup.html',context=context) 
        else:   
            return render(request,'mypanel/user/usergroup.html',context)
        
    except Exception as e:  
        return Response_errorhandler('PostUserGroup', request, e)
    
# DATATABLES FUNCTION::
def GetAllUserGroup(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        if not user_id or not token:
            return redirect('login')
        
        data_tbl = dict(request.GET)    
        headers = {
            'Authorization': f'Bearer {token}'
        }
        params = {'data_table':json.dumps(data_tbl),}

        user_list = requests.get('{url}/common/usergroupmenudatatable/'.format(url=url), params=params, headers=headers).json()
        return JsonResponse(user_list, safe=False)
    
    except Exception as e:  
        return Response_errorhandler('GetAllUserGroup', request, e)


# DELETE FUNCTION ::
def DeleteUserGroup(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        if not user_id or not token:
            return redirect('login')

        usergroup_id = request.GET.get('usergroup_id')
        params =  {"usergroup_id": usergroup_id,'user_id':user_id}
        headers = {
            'Authorization': f'Bearer {token}'
        }

        usergroup=requests.delete('{url}/common/deleteusergroupmenu/'.format(url=url),params=params, headers=headers)
        if  usergroup.status_code == 202:
            messages.success(request,'Usergroup deleted successfully')
            return redirect('usergroup')
        else:
            msg=usergroup.json()
            messages.error(request,msg.get('message'))
            return redirect('usergroup')
    except Exception as e:  
        return Response_errorhandler('DeleteUserGroup', request, e)

# USER Profile functions ::
def user_profile_screen(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        if not user_id or not token:
            return redirect('login')
        headers = {
            'Authorization': f'Bearer {token}'
        }
        params = {'user_id':user_id}
        userData = requests.get('{url}/user/get-userprofile-picture/'.format(url=url), params=params,headers=headers).json()
        return render(request,'mypanel/user/profile.html',{'userData':userData})
    
    except Exception as e:  
        return Response_errorhandler("user_profile_screen", request, e)
    
# Update user password ::
def update_user_password(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        if not user_id or not token:
            return redirect('login')
        
        headers = {
            'Authorization': f'Bearer {token}'
        }
        params = {'user_id':user_id}

        if request.method == 'POST':
            old_password = request.POST.get('txtOldPassword')
            new_password = request.POST.get('txtNewPassword')
            confirm_password = request.POST.get('txtConfirmPassword')

            if new_password == confirm_password:

                data = {
                    'old_password': old_password,
                    'new_password': new_password
                }
                put = requests.put('{url}/user/user-password-update/'.format(url=url),data=data, params=params,headers=headers)
                if put.status_code == status.HTTP_200_OK:
                    messages.success(request,CommonMessages.update('Password'))
                    return redirect('user-profile')
                else:
                    update_error = put.json()
                    error = update_error.get('error_message')
                    messages.error(request,error)
                    userData = requests.get('{url}/user/get-userprofile-picture/'.format(url=url), params=params,headers=headers).json()
                    return render(request, 'mypanel/user/profile.html', {'userData':userData, 'errors':error})
            else:
                messages.error(request,'Password is incorrect')
                return redirect('user-profile')
        else:
            return redirect('user-profile')
    except Exception as e:  
        return Response_errorhandler("update_user_password", request, e)

# USER Profile functions ::
def update_profile_picture(request):

    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        if not user_id or not token:
            return redirect('login')
        
        headers = {
            'Authorization': f'Bearer {token}'
        }
        params = {'user_id':user_id}
        userData = requests.get('{url}/user/get-userprofile-picture/'.format(url=url), params=params,headers=headers).json()

        if request.method == 'POST':

            file = {
                'profile_image':request.FILES.get('userProfileImg')
            }
            put = requests.put('{url}/user/update-userprofile-picture/'.format(url=url),files=file, params=params,headers=headers)
            
            if put.status_code == status.HTTP_200_OK:
                put_data = put.json()
                request.session['profile_image']= put_data.get('profileImg')
                messages.success(request,CommonMessages.update('Profile'))
                return redirect('user-profile')
            
            else:
                error = put.json()
                messages.error(request,CommonMessages.failed('Profile'))
                userData = requests.get('{url}/user/get-userprofile-picture/'.format(url=url), params=params).json()
                return render(request, 'mypanel/user/profile.html', {'userData':userData, 'errors':error})

        else:
            context = {"userData": userData}
            return render(request, 'mypanel/user/profile.html', context=context)
        
    except Exception as e:  
        return Response_errorhandler("update_profile_picture", request, e)

# Update display name
def update_display_name(request):

    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        if not user_id or not token:
            return redirect('login')
        
        headers = {
            'Authorization': f'Bearer {token}'
        }
        
        params = {'user_id':user_id}
        userData = requests.get('{url}/user/get-userprofile-picture/'.format(url=url), params=params,headers=headers).json()

        if request.method == 'POST':

            data = {'username':request.POST.get('txtUserName'),
                    'display_name':request.POST.get('txtDisplayName'),
                    'email':request.POST.get('txtUserEmail')
                    }
            put = requests.put('{url}/user/get-userprofile-picture/'.format(url=url),data=data, params=params,headers=headers)
            
            if put.status_code == status.HTTP_200_OK:
                put_data = put.json()
                request.session['display_name']=put_data.get('display_name')
                request.session['email']=put_data.get('email')
                messages.success(request,CommonMessages.update('User'))
                return  redirect('user-profile')
                
            else:
                error = put.json()
                messages.error(request,CommonMessages.update('User'))
                userData = requests.get('{url}/user/get-userprofile-picture/'.format(url=url), params=params,headers=headers).json()
                return render(request, 'mypanel/user/profile.html', {'userData':userData, 'errors':error})

        else:
            userData = requests.get('{url}/user/get-userprofile-picture/'.format(url=url), params=params,headers=headers).json()
            return render(request, 'mypanel/user/profile.html', {'userData':userData, 'errors':error})
        
    except Exception as e:  
        return Response_errorhandler("update_display_name", request, e)