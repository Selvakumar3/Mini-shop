import traceback
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import requests
import json
from rest_framework import status
from flourishapp.utils import *
url = settings.API_URL

# Stock Opening ::
def stock_opening_screen(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        # Redirect to login if user is not authenticated
        if not user_id or not token:
            return redirect('login')

        headers = {'Authorization': f'Bearer {token}'}

        # Fetch product and units
        product = getproduct(headers)
        unit = getunit(headers)
        get_batch_no = generate_batch_no('BAT')
        context = {'product':product,'unit':unit,'get_batch_no':get_batch_no}
         
        if request.method == 'POST':

            # Extract data from the request
            product_id = int(request.POST.get('ddlProduct'))
            total_qty = request.POST.get('txtTotalQty')
            expired_date = request.POST.get('txtDOE')
            sales_amt = request.POST.get('txtSalesPrice')
            convertion_value = request.POST.get('hdnConvertionValue')
            batch_no = request.POST.get('txtBatchNumber')

            #Convert date format ::
            exp_date = formatted_date(expired_date)

            data = {
                'product': product_id,
                'unit': int(request.POST.get('ddlUnit')) if request.POST.get('ddlUnit') else None,
                'convertion_value': int(convertion_value),
                'batch_no': batch_no,
                'total_qty': total_qty,
                'expire_date': exp_date,
                'sales_amount': sales_amt,
                'created_by': user_id,
            }
            post_response = requests.post(f'{url}/store/post-stockopening/',data=data,headers=headers)

            if post_response.status_code == status.HTTP_201_CREATED:
                messages.success(request, CommonMessages.create('Stock'))
                return redirect('stock')
            else:
                error = post_response.json()
                messages.error(request, CommonMessages.create_failed('Stock'))
                return render(request, 'mypanel/store/stock_opening.html', {'errors': error,'data': data,'product':product,'unit': unit})
        else:
            return render(request, 'mypanel/store/stock_opening.html', context)

    except Exception as e:
        return Response_errorhandler("stock_opening_screen", request, e)

# Stock Datatable ::
def stock_opening_dt(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        if not user_id or not token:
            return redirect('login')
        
        headers = {'Authorization': f'Bearer {token}'}
        data_tbl = dict(request.GET)
        start_date = request.GET.get('start_date') 
        end_date = request.GET.get('end_date')
        product_id = request.GET.get('product_id')
        params = {
            'user':user_id, 
            'data_table': json.dumps(data_tbl),
            'start_date':start_date,
            'end_date':end_date,
            'product_id':product_id,
        }
        
        data = requests.get('{url}/store/stockopening-dt'.format(url=url),params=params,headers=headers).json()
        return JsonResponse(data, safe=False)
    
    except Exception as e:
        return Response_errorhandler("stock_dt", request, e)
    
# Stock List Datatable ::
def stock_list_dt(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        if not user_id or not token:
            return redirect('login')
        
        headers = {'Authorization': f'Bearer {token}'}
        data_tbl = dict(request.GET)
        start_date = request.GET.get('start_date') 
        end_date = request.GET.get('end_date')
        product_id = request.GET.get('product_id')
        stock_id = request.GET.get('stock_id')
        params = {
            'user':user_id, 
            'data_table': json.dumps(data_tbl),
            'start_date':start_date,
            'end_date':end_date,
            'product_id':product_id,
            'stock_id':stock_id,
        }
        
        data = requests.get('{url}/store/get-stock-dt'.format(url=url),params=params,headers=headers).json()
        return JsonResponse(data, safe=False)
    
    except Exception as e:
        return Response_errorhandler("stock_list_dt", request, e)
    
# Delete Stock Opening ::
def delete_stock_opening(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        if not user_id or not token:
            return redirect('login')
        
        headers = {
            'Authorization': f'Bearer {token}'
        }
        opening_id = request.GET.get('opening_id')
        params = {"opening_id":opening_id}

        delete = requests.delete('{url}/store/delete-stockopening/'.format(url=url),params=params,headers=headers)

        if delete.status_code == status.HTTP_200_OK:
            messages.success(request,CommonMessages.delete('Stock opening'))
            return redirect('stock')
        
        elif delete.status_code == status.HTTP_400_BAD_REQUEST :
            errors = delete.json()
            error = errors['message']
            messages.error(request,error)
            return redirect('stock')
        else:
            messages.error(request,CommonMessages.delete_failed('Stock opening'))
            return redirect('stock')
        
    except Exception as e:
        return Response_errorhandler("delete_stock_opening", request, e)
    
def stock_list_screen(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        # Redirect to login if user is not authenticated
        if not user_id or not token:
            return redirect('login')
        headers = {'Authorization': f'Bearer {token}'}
        # Fetch product and units
        product = getproduct(headers)
        context = {'product':product}
        return render(request,'mypanel/store/stock_list.html',context)
    except Exception as e:
        return Response_errorhandler("stock_list_screen", request, e)
