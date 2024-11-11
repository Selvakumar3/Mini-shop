import traceback
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import requests
import json
from rest_framework import status
from flourishapp.utils import *
url = settings.API_URL
api_img_url = settings.API_IMG_URL


# Get Poa data ::
def pos_data(request):

    user_id = request.session.get('user_id')
    token = request.session.get('token')
    headers = {'Authorization': f'Bearer {token}'}
    # Fetch API
    category = getcategories(headers)
    billtype = get_billtype(headers)
    admin_settings = get_admin_settings(headers)
    generatecode = get_code(headers,'INV')
    context = {'category':category,'billtype':billtype,'generatecode':generatecode,'api_img_url':api_img_url,'admin_settings':admin_settings}
    return context

# POS screen ::
def pos_screen(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        # Redirect to login if user is not authenticated
        if not user_id or not token:
            return redirect('login')

        headers = {'Authorization': f'Bearer {token}'}

        # Fetch API data
        category = getcategories(headers)
        billtype = get_billtype(headers)
        admin_settings = get_admin_settings(headers)
        generatecode = get_code(headers,'INV')

        context = {'category':category,'billtype':billtype,'generatecode':generatecode,'api_img_url':api_img_url,'admin_settings':admin_settings}

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

                edit_id = request.POST.get('hiddenPosId')
                data.update({'updated_by': user_id,'updated_at':dt})

                params = {'pos_id': edit_id}
                update_purchase_invoice = requests.put(f'{url}/store/update-pos/', data=data,params=params,headers=headers)
                
                if update_purchase_invoice.status_code == status.HTTP_200_OK:
                    messages.success(request, CommonMessages.update('POS'))
                    return redirect('pos-list')
                else:
                    error = update_purchase_invoice.json()
                    messages.error(request, CommonMessages.failed('POS'))
                    return render(request, 'mypanel/store/pos.html', {'errors': error, 'data': data,'edit':'edit','pos_id':edit_id}) 

            # Create action
            else:
                data.update({
                'pos_no':  request.POST.get('txtInvoiceNo'),
                'pos_date':formatted_date(request.POST.get('txtInvoiceDate')),
                'created_by': user_id
                })

                post_purchase_invoice = requests.post(f'{url}/store/post-pos/',data=data,headers=headers)

                if post_purchase_invoice.status_code == status.HTTP_201_CREATED:
                    messages.success(request, CommonMessages.create('POS'))
                    return redirect('pos-list')
                else:
                    error = post_purchase_invoice.json()
                    messages.error(request, CommonMessages.create_failed('POS'))
                    return render(request, 'mypanel/store/pos.html', {'errors': error, 'data': data})
        else:
            return render(request,'mypanel/store/pos.html',context)
        
    except Exception as e:
        return Response_errorhandler("pos_screen", request, e)
    
# Purchase invoice List ::
def pos_list_screen(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        # Redirect to login if user is not authenticated
        if not user_id or not token:
            return redirect('login')
        return render(request,'mypanel/store/pos_list.html')
    except Exception as e:
        return Response_errorhandler("pos_list_screen", request, e)
    
# Get Pos Details
def getPosDetails(request):
    try:
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        # Redirect to login if user is not authenticated
        if not user_id or not token:
            return redirect('login')

        headers = {'Authorization': f'Bearer {token}'}
        pos_id = request.GET.get('hiddenPosId')
        
        params = {'pos_id': pos_id,'user_id':user_id}
        getPos = requests.get('{url}/store/get-pos-edit/'.format(url=url),params=params,headers=headers).json()
        pos_Det = getPos.get('posDetails')
       
        json_est_det = json.dumps(pos_Det)
        
        data ={
                'pos_no':getPos['pos_no'],
                'pos_date':getPos['pos_date'],
                'sub_total':getPos['sub_total'],
                'round_off':getPos['round_off'],
                'net_amount':getPos['net_amount'],
                'paid_amount':getPos['paid_amount'],
                'bill_type':getPos['bill_type'],
                'notes':getPos['notes'],
                'itemdetail':json_est_det,
                'pos_id':pos_id,
                'pos_Det':pos_Det,
            }
        context = pos_data(request)
        context['transpos'] = getPos 
        context['edit'] = 'edit' 
        context['data'] = data 
        return render(request,'mypanel/store/pos.html',context=context)

    except Exception as e:
       return Response_errorhandler("getPosDetails", request, e)
    
# Delete Pos
def deletePos(request):
    try: 
        user_id = request.session.get('user_id')
        token = request.session.get('token')

        # Redirect to login if user is not authenticated
        if not user_id or not token:
            return redirect('login')

        headers = {'Authorization': f'Bearer {token}'}
        params = {'pos_id': request.GET.get('pos_id'), 'user':user_id}

        delete = requests.delete('{url}/store/delete-pos/'.format(url=url),params=params, headers=headers)

        if delete.status_code == status.HTTP_200_OK:
            messages.success(request,CommonMessages.delete('POS'))
            return redirect('pos-list')
        else:
            del_err = delete.json()
            messages.error(request,CommonMessages.delete_failed('POS'))
            return redirect('pos-list')
    
    except Exception as e:
        return Response_errorhandler("deletePos", request, e)
    
# Pos Datatable
def PosDatatable(request):
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
        
        data = requests.get('{url}/store/pos-dt/'.format(url=url),headers=headers,params=params).json()
        return JsonResponse(data, safe=False)

    except Exception as e:
        return Response_errorhandler("PosDatatable", request, e)