import traceback
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import requests
import json
from rest_framework import status
from flourishapp.utils import *
url = settings.API_URL

# Get Purchase invoice data ::
def purchaseInvoice_data(request):
    user_id = request.session.get('user_id')
    token = request.session.get('token')
    headers = {'Authorization': f'Bearer {token}'}
    # Fetch API
    product = getproduct(headers)
    unit = getunit(headers)
    billtype = get_billtype(headers)
    generatecode = get_code(headers,'PUR')
    context = {'product':product,'unit':unit,'generatecode':generatecode,'billtype':billtype}
    return context

# Post & Put Purchase invoice  ::
def purchase_invoice_screen(request):
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
        billtype = get_billtype(headers)
        generatecode = get_code(headers,'PUR')
        context = {'product':product,'unit':unit,'generatecode':generatecode,'billtype':billtype}

        if request.method == 'POST':
            itemdetail=request.POST.get('itemdetail')

            data = {
                'sub_total':request.POST.get('subTotal'),
                'round_off':request.POST.get('roundOff'),
                'net_amount':request.POST.get('netAmount'),
                'paid_amount':request.POST.get('netAmount'),
                'bill_type':int(request.POST.get('ddlBillType')),
                'notes':request.POST.get('notes'),
                'itemdetail':itemdetail,    # json data to dump
            }

            # Update action
            if request.POST.get('hiddenEdit') == 'edit':

                edit_id = request.POST.get('hiddenPurchaseId')
                data.update({'updated_by': user_id,'updated_at':dt})

                params = {'purchase_id': edit_id}
                update_purchase_invoice = requests.put(f'{url}/store/update-purchase-invoice/', data=data,params=params,headers=headers)
                
                if update_purchase_invoice.status_code == status.HTTP_200_OK:
                    messages.success(request, CommonMessages.update('Purchase invoice'))
                    return redirect('purchase-invoice-list')
                else:
                    error = update_purchase_invoice.json()
                    messages.error(request, CommonMessages.failed('Purchase invoice'))
                    return render(request, 'mypanel/store/purchase_invoice.html', {'errors': error, 'data': data,'edit':'edit','purchase_id':edit_id}) 

            # Create action
            else:
                data.update({
                'purchase_no':  request.POST.get('txtPurchaseno'),
                'purchase_date':formatted_date(request.POST.get('txtPurchaseDate')),
                'created_by': user_id
                })

                post_purchase_invoice = requests.post(f'{url}/store/post-purchase-invoice/',data=data,headers=headers)

                if post_purchase_invoice.status_code == status.HTTP_201_CREATED:
                    messages.success(request, CommonMessages.create('Purchase invoice'))
                    return redirect('purchase-invoice-list')
                else:
                    error = post_purchase_invoice.json()
                    messages.error(request, CommonMessages.create_failed('Purchase invoice'))
                    return render(request, 'mypanel/store/purchase_invoice.html', {'errors': error, 'data': data})
        else:
            return render(request,'mypanel/store/purchase_invoice.html',context)
        
    except Exception as e:
        return Response_errorhandler("purchase_invoice_screen", request, e)

# Purchase invoice List ::
def purchase_invoice_list_screen(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        # Redirect to login if user is not authenticated
        if not user_id or not token:
            return redirect('login')
        return render(request,'mypanel/store/purchase_invoice_list.html')
    except Exception as e:
        return Response_errorhandler("purchase_invoice_screen", request, e)

# Get Purchase invoice Details
def getPurchaseDetails(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        # Redirect to login if user is not authenticated
        if not user_id or not token:
            return redirect('login')

        headers = {'Authorization': f'Bearer {token}'}
        purchase_id = request.GET.get('hiddenPurchaseId')
        
        params = {'purchase_id': purchase_id,'user_id':user_id}
        getPurchase = requests.get('{url}/store/get-purchase-edit/'.format(url=url),params=params,headers=headers).json()
        purchase_Det = getPurchase.get('purchaseDet')
        # for i in purchase_Det:
        #     i['net_amount'] = str(i['net_amount'])
             
        json_est_det = json.dumps(purchase_Det)
        
        data ={
                'purchase_no':getPurchase['purchase_no'],
                'purchase_date':getPurchase['purchase_date'],
                'sub_total':getPurchase['sub_total'],
                'round_off':getPurchase['round_off'],
                'net_amount':getPurchase['net_amount'],
                'paid_amount':getPurchase['paid_amount'],
                'bill_type':getPurchase['bill_type'],
                'notes':getPurchase['notes'],
                'itemdetail':json_est_det,
                'purchase_id':purchase_id,
                'purchase_Det':purchase_Det,
            }
        context = purchaseInvoice_data(request)
        context['transPurchase'] = getPurchase 
        context['edit'] = 'edit' 
        context['data'] = data 
        return render(request,'mypanel/store/purchase_invoice.html',context=context)

    except Exception as e:
       return Response_errorhandler("getPurchaseDetails", request, e)
    
# Delete Purchase invoice 
def deletePurchaseInvoice(request):
    try: 
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        # Redirect to login if user is not authenticated
        if not user_id or not token:
            return redirect('login')

        headers = {'Authorization': f'Bearer {token}'}
        params = {'purchase_id': request.GET.get('purchase_id'), 'user':user_id}

        delete = requests.delete('{url}/store/delete-purchase-invoice/'.format(url=url),params=params, headers=headers)

        if delete.status_code == status.HTTP_200_OK:
            messages.success(request,CommonMessages.delete('Purchase invoice'))
            return redirect('purchase-invoice-list')
        else:
            del_err = delete.json()
            messages.error(request,CommonMessages.delete_failed('Purchase invoice'))
            return redirect('purchase-invoice-list')
    
    except Exception as e:
        return Response_errorhandler("deletePurchaseInvoice", request, e)
    
# Purchase invoice Datatable
def PurchaseDatatable(request):
    try: 
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        # Redirect to login if user is not authenticated
        if not user_id or not token:
            return redirect('login')

        headers = {'Authorization': f'Bearer {token}'}
        data_tbl = dict(request.GET)
        start_date = request.GET.get('start_date') 
        end_date = request.GET.get('end_date')
        bill_type = request.GET.get('bill_type')
        params = {
                'user':user_id, 
                'data_table': json.dumps(data_tbl),
                'start_date':start_date,
                'end_date':end_date,
                'bill_type':bill_type
                }
        data = requests.get('{url}/store/purchase-dt/'.format(url=url),headers=headers,params=params).json()
        return JsonResponse(data, safe=False)

    except Exception as e:
        return Response_errorhandler("PurchaseDatatable", request, e)
    

def Purchase_product_detail(request):
    try: 
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        # Redirect to login if user is not authenticated
        if not user_id or not token:
            return redirect('login')

        headers = {'Authorization': f'Bearer {token}'}
        purchase_id = request.GET.get('purchase_id')
        params = {
                'purchase_id':purchase_id,
                }
        data = requests.get('{url}/store/purchasedet-detail/'.format(url=url),headers=headers,params=params).json()
        return JsonResponse(data, safe=False)
    
    except Exception as e:
        return Response_errorhandler("Purchase_product_detail", request, e)
    
def get_stock_available(request):
    try: 
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        # Redirect to login if user is not authenticated
        if not user_id or not token:
            return redirect('login')

        headers = {'Authorization': f'Bearer {token}'}
        batch_no = request.GET.get('batch_no')
        params = {
                'batch_no':batch_no,
            }
        data = requests.get('{url}/store/get-stock-qty/'.format(url=url),headers=headers,params=params).json()
        return JsonResponse(data, safe=False)
    
    except Exception as e:
        return Response_errorhandler("get_stock_available", request, e)
    

def get_product_batch_no(request):
    try: 
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        # Redirect to login if user is not authenticated
        if not user_id or not token:
            return redirect('login')

        headers = {'Authorization': f'Bearer {token}'}
        product_id = request.GET.get('product_id')
        params = {
                'product_id':product_id,
            }
        data = requests.get('{url}/store/get-product-batch/'.format(url=url),headers=headers,params=params).json()
        return JsonResponse(data, safe=False)
    
    except Exception as e:
        return Response_errorhandler("get_product_batch_no", request, e)

