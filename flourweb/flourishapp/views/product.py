import traceback
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import requests
import json
from rest_framework import status
from flourishapp.utils import *
url = settings.API_URL

# Product Screen ::
def product_screen(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        # Redirect to login if user is not authenticated
        if not user_id or not token:
            return redirect('login')

        headers = {'Authorization': f'Bearer {token}'}
        
        # Fetch categories, brands, and units
        category = getcategories(headers)
        brand = getbrand(headers)
        unit = getunit(headers)

        if request.method == 'POST':
            # Extract data from the request
            product_name = request.POST.get('txtProductName')
            category_name = int(request.POST.get('ddlCategory'))
            brand_id = int(request.POST.get('ddlBrand'))
            unit_id = int(request.POST.get('ddlUnit'))
            product_image = request.FILES.get('productImg')
            mrp = request.POST.get('txtMRP')
            customer_price = request.POST.get('txtCustomerPrice')
            desc = request.POST.get('txtDescription')

            data = {
                'product_name': product_name,
                'category': category_name,
                'brand': brand_id,
                'unit': unit_id,
                'mrp': mrp,
                'customer_price': customer_price,
                'desc': desc,
                'is_active': True,
            }

            # Prepare file upload if there is an image
            files = {'product_image': product_image} if product_image else {}

            # Determine if we're editing an existing product
            if request.POST.get('hiddenEdit') == 'edit':
                edit_id = request.POST.get('hiddeProductId')
                data.update({'updated_by': user_id, 'updated_at': dt})

                params = {'product_id': edit_id}
                update_response = requests.put(
                    f'{url}/masters/edit-product/',
                    data=data,
                    files=files,
                    params=params,
                    headers=headers
                )

                if update_response.status_code == status.HTTP_200_OK:
                    messages.success(request, CommonMessages.update('Product'))
                    return redirect('product-list')
                else:
                    error = update_response.json()
                    messages.error(request, CommonMessages.failed('Product'))
                    return render(request, 'mypanel/master/product.html', {
                        'errors': error,
                        'data': data,
                        'edit': 'edit',
                        'category': category,
                        'brand': brand,
                        'unit': unit,
                        'product_id': edit_id
                    })

            # Create new product
            else:
                data.update({'created_by': user_id})
                post_response = requests.post(
                    f'{url}/masters/post-product/',
                    files=files,
                    data=data,
                    headers=headers
                )

                if post_response.status_code == status.HTTP_201_CREATED:
                    messages.success(request, CommonMessages.create('Product'))
                    return redirect('product-list')
                else:
                    error = post_response.json()
                    messages.error(request, CommonMessages.create_failed('Product'))
                    return render(request, 'mypanel/master/product.html', {
                        'errors': error,
                        'data': data,
                        'category': category,
                        'brand': brand,
                        'unit': unit
                    })

        else:  # GET request handling
            product_id = request.GET.get('product_id')
            context = {
                "category": category,
                "brand": brand,
                "unit": unit
            }
            if product_id is not None:
                context.update({"product_id": product_id})

            return render(request, 'mypanel/master/product.html', context)

    except Exception as e:
        return Response_errorhandler("product_screen", request, e)

# Product Datatable ::
def product_dt(request):
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
        
        data = requests.get('{url}/masters/product-dt-api'.format(url=url),params=params,headers=headers).json()
        return JsonResponse(data, safe=False)
    
    except Exception as e:
        return Response_errorhandler("product_dt", request, e)

# Edit Product ::
def edit_product(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        if not user_id or not token:
            return redirect('login')
        
        headers = {
            'Authorization': f'Bearer {token}'
        }
        product_id = request.GET.get('product_id')
        params = {"product_id":product_id}

        data = requests.get('{url}/masters/edit-product'.format(url=url),params=params,headers=headers).json()
        return JsonResponse(data, safe=False)
    
    except Exception as e:
        return Response_errorhandler("edit_product", request, e)
    
# Delete Product ::
def delete_product(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        if not user_id or not token:
            return redirect('login')
        
        headers = {
            'Authorization': f'Bearer {token}'
        }
        product_id = request.GET.get('product_id')
        params = {"product_id":product_id}

        delete = requests.delete('{url}/masters/delete-product/'.format(url=url),params=params,headers=headers)

        if delete.status_code == status.HTTP_200_OK:
            messages.success(request,CommonMessages.delete('Product'))
            return redirect('product-list')
        
        elif delete.status_code == status.HTTP_400_BAD_REQUEST :
            errors = delete.json()
            error = errors['message']
            messages.error(request,error)
            return redirect('product-list')
        else:
            messages.error(request,CommonMessages.delete_failed('Product'))
            return redirect('product-list')
    
    except Exception as e:
        return Response_errorhandler("delete_product", request, e)
    
# Update product status ::
def update_product_status(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        if not user_id or not token:
            return redirect('login')
        
        headers = {
            'Authorization': f'Bearer {token}'
        }
        product_id = request.GET.get("id")
        is_active = request.GET.get("sts")

        params = {"product_id": product_id, "is_active": is_active}

        updateFeatures = requests.put(
            "{url}/masters/update-product-status/".format(url=url), params=params,headers=headers
        )

        if updateFeatures.status_code == status.HTTP_200_OK:
            messages.success(request, CommonMessages.update_status("Product"))
            return redirect("product-list")

        else:
            messages.error(request, CommonMessages.failed("Product"))
            return redirect("product-list")
    
    except Exception as e:
        return Response_errorhandler("update_product_status", request, e)

# Product list Screen ::
def product_list_screen(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        # Redirect to login if user is not authenticated
        if not user_id or not token:
            return redirect('login')
        
        return render(request,'mypanel/master/product_list.html')
        
    except Exception as e:
        return Response_errorhandler("product_list_screen", request, e)
    
    