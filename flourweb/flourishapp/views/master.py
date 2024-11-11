import traceback
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import requests
import json
from rest_framework import status
from flourishapp.utils import *
url = settings.API_URL

# Category Post & Put ::
def category_screen(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        if not user_id or not token:
            return redirect('login')
        
        headers = {
            'Authorization': f'Bearer {token}'
        }
        
        if request.method == 'POST':
            category_name = request.POST.get('txtCategoryName')
            category_desc = request.POST.get('txtDescription')
            category_image = request.FILES.get('categoryImg')

            data = {
                'category_name': category_name,
                'category_desc': category_desc,
            }

            # IMAGES FILES FROM HTML
            files = {'category_image': category_image} if category_image else {}

            # Update action
            if request.POST.get('hiddenEdit') == 'edit':
                edit_id = request.POST.get('hiddenCategoryId')
                data.update({'updated_by': user_id,'updated_at':dt})

                params = {'category_id': edit_id}
                update_category = requests.put(f'{url}/masters/put-category/', data=data, files=files,params=params,headers=headers)
                
                if update_category.status_code == status.HTTP_200_OK:
                    messages.success(request, CommonMessages.update('Category'))
                else:
                    error = update_category.json()
                    messages.error(request, CommonMessages.failed('Category'))
                    return render(request, 'mypanel/master/category.html', {'errors': error, 'data': data,'edit':'edit','category_id':edit_id})

            # Create action
            else:
                data.update({'created_by': user_id,'is_active':True})
                post_category = requests.post(f'{url}/masters/post-category/',files=files, data=data,headers=headers)

                if post_category.status_code == status.HTTP_201_CREATED:
                    messages.success(request, CommonMessages.create('Category'))
                else:
                    error = post_category.json()
                    messages.error(request, CommonMessages.create_failed('Category'))
                    return render(request, 'mypanel/master/category.html', {'errors': error, 'data': data})

            return redirect('category')

        else:
            return render(request, 'mypanel/master/category.html')
    
    except Exception as e:
        return Response_errorhandler("category_screen", request, e)

# Category Datatable ::
def category_dt(request):
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
        
        data = requests.get('{url}/masters/category-dt-api'.format(url=url),params=params,headers=headers).json()
        return JsonResponse(data, safe=False)
    
    except Exception as e:
        return Response_errorhandler("category_dt", request, e)

# Edit Category ::
def edit_category(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        if not user_id or not token:
            return redirect('login')
        
        headers = {
            'Authorization': f'Bearer {token}'
        }
        category_id = request.GET.get('category_id')
        params = {"category_id":category_id}

        data = requests.get('{url}/masters/edit-category'.format(url=url),params=params,headers=headers).json()
        return JsonResponse(data, safe=False)
    
    except Exception as e:
        return Response_errorhandler("edit_category", request, e)
    
# Delete Category ::
def delete_category(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        if not user_id or not token:
            return redirect('login')
        
        headers = {
            'Authorization': f'Bearer {token}'
        }
        category_id = request.GET.get('category_id')
        params = {"category_id":category_id}

        delete = requests.delete('{url}/masters/delete-category/'.format(url=url),params=params,headers=headers)

        if delete.status_code == status.HTTP_200_OK:
            messages.success(request,CommonMessages.delete('Category'))
            return redirect('category')
        
        elif delete.status_code == status.HTTP_400_BAD_REQUEST :
            errors = delete.json()
            error = errors['message']
            messages.error(request,error)
            return redirect('category')
        else:
            messages.error(request,CommonMessages.delete_failed('Category'))
            return redirect('category')
    
    except Exception as e:
        return Response_errorhandler("delete_category", request, e)
    
# Update Category status ::
def update_category_status(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        if not user_id or not token:
            return redirect('login')
        
        headers = {
            'Authorization': f'Bearer {token}'
        }
        category_id = request.GET.get("id")
        is_active = request.GET.get("sts")

        params = {"category_id": category_id, "is_active": is_active}

        updateFeatures = requests.put(
            "{url}/masters/update-category-status/".format(url=url), params=params,headers=headers
        )

        if updateFeatures.status_code == status.HTTP_200_OK:
            messages.success(request, CommonMessages.update_status("Category"))
            return redirect("category")

        else:
            messages.error(request, CommonMessages.failed("Category"))
            return redirect("category")
    
    except Exception as e:
        return Response_errorhandler("update_category_status", request, e)
    

# Brand Screen Post & Put::
def brand_screen(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        if not user_id or not token:
            return redirect('login')
        
        headers = {
            'Authorization': f'Bearer {token}'
        }
        category = getcategories(headers)
      
        if request.method == 'POST':
            brand_name = request.POST.get('txtBrandName')
            category_name = int(request.POST.get('ddlCategory'))
            brand_image = request.FILES.get('brandImg')

            data = {
                'brand_name': brand_name,
                'category': category_name,
            }

            # IMAGES FILES FROM HTML
            files = {'brand_image': brand_image} if brand_image else {}

            # Update action
            if request.POST.get('hiddenEdit') == 'edit':
                edit_id = request.POST.get('hiddenBrandId')
                data.update({'updated_by': user_id,'updated_at':dt})

                params = {'brand_id': edit_id}
                update_brand = requests.put(f'{url}/masters/put-brand/', data=data, files=files,params=params,headers=headers)
                
                if update_brand.status_code == status.HTTP_200_OK:
                    messages.success(request, CommonMessages.update('Brand'))
                else:
                    error = update_brand.json()
                    messages.error(request, CommonMessages.failed('Brand'))
                    return render(request, 'mypanel/master/brand.html', {'errors': error, 'data': data,'edit':'edit',"category": category,'brand_id':edit_id})

            # Create action
            else:
                data.update({'created_by': user_id,'is_active':True})
                post_brand = requests.post(f'{url}/masters/post-brand/',files=files, data=data,headers=headers)

                if post_brand.status_code == status.HTTP_201_CREATED:
                    messages.success(request, CommonMessages.create('Brand'))
                else:
                    error = post_brand.json()
                    messages.error(request, CommonMessages.create_failed('Brand'))
                    return render(request, 'mypanel/master/brand.html', {'errors': error, 'data': data,"category": category})

            return redirect('brand')

        else:
            return render(request, 'mypanel/master/brand.html',{"category": category})
    
    except Exception as e:
        return Response_errorhandler("brand_screen", request, e)
   
# Brand Datatable ::
def brand_dt(request):
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
        
        data = requests.get('{url}/masters/brand-dt-api'.format(url=url),params=params,headers=headers).json()
        return JsonResponse(data, safe=False)
    
    except Exception as e:
        return Response_errorhandler("brand_dt", request, e)

# Edit Brand ::
def edit_brand(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        if not user_id or not token:
            return redirect('login')
        
        headers = {
            'Authorization': f'Bearer {token}'
        }
        brand_id = request.GET.get('brand_id')
        params = {"brand_id":brand_id}

        data = requests.get('{url}/masters/edit-brand'.format(url=url),params=params,headers=headers).json()
        return JsonResponse(data, safe=False)
    
    except Exception as e:
        return Response_errorhandler("edit_brand", request, e)
    
# Delete Brand ::
def delete_brand(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        if not user_id or not token:
            return redirect('login')
        
        headers = {
            'Authorization': f'Bearer {token}'
        }
        brand_id = request.GET.get('brand_id')
        params = {"brand_id":brand_id}

        delete = requests.delete('{url}/masters/delete-brand/'.format(url=url),params=params,headers=headers)

        if delete.status_code == status.HTTP_200_OK:
            messages.success(request,CommonMessages.delete('Brand'))
            return redirect('brand')
        
        elif delete.status_code == status.HTTP_400_BAD_REQUEST :
            errors = delete.json()
            error = errors['message']
            messages.error(request,error)
            return redirect('brand')
        else:
            messages.error(request,CommonMessages.delete_failed('Brand'))
            return redirect('brand')
    
    except Exception as e:
        return Response_errorhandler("delete_brand", request, e)
    
# Update Brand status ::
def update_brand_status(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        if not user_id or not token:
            return redirect('login')
        
        headers = {
            'Authorization': f'Bearer {token}'
        }
        brand_id = request.GET.get("id")
        is_active = request.GET.get("sts")

        params = {"brand_id": brand_id, "is_active": is_active}

        updateFeatures = requests.put(
            "{url}/masters/update-brand-status/".format(url=url), params=params,headers=headers
        )

        if updateFeatures.status_code == status.HTTP_200_OK:
            messages.success(request, CommonMessages.update_status("Brand"))
            return redirect("brand")

        else:
            messages.error(request, CommonMessages.failed("Brand"))
            return redirect("brand")
    
    except Exception as e:
        return Response_errorhandler("update_brand_status", request, e)

# Unit Screen ::
def unit_screen(request):
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
                'unit_name': request.POST.get('txtUnitName'),
                'is_active':True
            }

            # Update action
            if request.POST.get('hiddenEdit') == 'edit':
                edit_id = request.POST.get('hiddenUnitId')
                data.update({'updated_by': user_id,'updated_at':dt})

                params = {'unit_id': edit_id}
                update_category = requests.put(f'{url}/masters/put-unit/', data=data,params=params,headers=headers)
                
                if update_category.status_code == status.HTTP_200_OK:
                    messages.success(request, CommonMessages.update('Unit'))
                else:
                    error = update_category.json()
                    messages.error(request, CommonMessages.failed('Unit'))
                    return render(request, 'mypanel/master/unit.html', {'errors': error,'data': data,'edit':'edit','unit_id':edit_id})

            # Create action
            else:
                data.update({'created_by': user_id})
                post_category = requests.post(f'{url}/masters/post-unit/',data=data,headers=headers)

                if post_category.status_code == status.HTTP_201_CREATED:
                    messages.success(request, CommonMessages.create('Unit'))
                else:
                    error = post_category.json()
                    messages.error(request, CommonMessages.create_failed('Unit'))
                    return render(request, 'mypanel/master/unit.html', {'errors': error, 'data': data})

            return redirect('unit')

        else:
            return render(request, 'mypanel/master/unit.html')
    
    except Exception as e:
        return Response_errorhandler("unit_screen", request, e)
 
# Edit Unit ::
def edit_unit(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        if not user_id or not token:
            return redirect('login')
        
        headers = {
            'Authorization': f'Bearer {token}'
        }
        unit_id = request.GET.get('unit_id')
        params = {"unit_id":unit_id}

        data = requests.get('{url}/masters/edit-unit'.format(url=url),params=params,headers=headers).json()
        return JsonResponse(data, safe=False)
    
    except Exception as e:
        return Response_errorhandler("edit_unit", request, e)

# Delete Unit ::
def delete_unit(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        if not user_id or not token:
            return redirect('login')
        
        headers = {
            'Authorization': f'Bearer {token}'
        }
        unit_id = request.GET.get('unit_id')
        params = {"unit_id":unit_id}

        delete = requests.delete('{url}/masters/delete-unit/'.format(url=url),params=params,headers=headers)

        if delete.status_code == status.HTTP_200_OK:
            messages.success(request,CommonMessages.delete('Unit'))
            return redirect('unit')
        
        elif delete.status_code == status.HTTP_400_BAD_REQUEST :
            errors = delete.json()
            error = errors['message']
            messages.error(request,error)
            return redirect('unit')
        else:
            messages.error(request,CommonMessages.delete_failed('Unit'))
            return redirect('unit')
    
    except Exception as e:
        return Response_errorhandler("delete_unit", request, e)

# Unit Datatable ::
def unit_dt(request):
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
        
        data = requests.get('{url}/masters/unit-dt-api'.format(url=url),params=params,headers=headers).json()
        return JsonResponse(data, safe=False)
    
    except Exception as e:
        return Response_errorhandler("unit_dt", request, e)

# Product Screen ::
def product_screen(request):
    return render(request,'mypanel/master/product.html')