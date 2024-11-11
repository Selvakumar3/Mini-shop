from rest_framework.views import APIView
from flourishapi.serializers.store import *
from flourishapi.models import *
from flourishapi.utils import *
from flourishapi import datatable
from rest_framework.response import Response
from rest_framework import status
from django.db.models import RestrictedError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
import json
import requests
from django.db import transaction
from django.db.models import F

# Unit Amt Calculation ::
def unitamountcalucaltion(sales_amount,convertion_value):
    unitSalesAmount = float(sales_amount)/int(convertion_value)
    return unitSalesAmount

# STOCK OPENING ::
class StockOpeningAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        """
        Summary or Description of the function:
           create stock opening
        Parameter: No Parameter
        Method: 'POST'
        Response: 'JsonResponse'
        Output:{
            if data okay: returns 202 status code, with data.
            else: returns 400 status code, with validation error.
        }

        """
        try:
            serializer_class = StockOpeningSerializer(data=request.data)
            if serializer_class.is_valid():
                with transaction.atomic():
                    Serializerdetail = serializer_class.save()
                    opening_id = Serializerdetail.opening_id
                    product_id = request.data.get('product')
                    batch_no = request.data.get('batch_no')
                    total_qty = request.data.get('total_qty')
                    expire_date = request.data.get('expire_date')
                    sales_amount = request.data.get('sales_amount')
                    unit_id = request.data.get('unit')
                    created_by = request.data.get('created_by')
                    convertion_value = int(request.data.get('convertion_value'))
                    total_qty = int(request.data.get('total_qty'))
                    total_qty = total_qty * convertion_value
            
                    unit_sales_amount = unitamountcalucaltion(sales_amount,convertion_value)
                    #To update stock if batch already exists
                    if stock.objects.filter(batch_no = batch_no,product=product_id).exists():
                        stock.objects.filter(batch_no = batch_no).update(
                            stock_qty=F('stock_qty') + total_qty,
                            total_qty = F('total_qty') + total_qty,
                            sales_amount=sales_amount,
                            unit_sales_amount=unit_sales_amount,
                            unit=unit_id)
                    else:
                        stock.objects.create(
                            product_id=product_id,
                            batch_no=batch_no,
                            stock_qty=total_qty,
                            total_qty=total_qty,
                            expire_date=expire_date,
                            sales_amount=sales_amount,
                            unit_sales_amount=unit_sales_amount,
                            unit_id=unit_id,
                            created_at=date_time,
                            )   
                    
                        admin_settings = AdminSettings.objects.first()
                        if admin_settings:
                            admin_settings.stock_update_at = date_time
                            admin_settings.save()

                    stock_id = stock.objects.get(batch_no=batch_no,product=product_id).stock_id
                    
                    Opening.objects.filter(opening_id=opening_id).update(stock_id=stock_id)
                return Response(serializer_class.data, status=status.HTTP_201_CREATED)
            else: 
                return error_response.serializer_error(self.__class__.__name__, request, serializer_class)

        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)
        
# Delete STOCK ::
class StockOpeningDeleteAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
   
    def delete(self, request):
        """
            Summary or Description of the Function:
                * Delete an stock opening details By openingId.
            Parameters:
                openingId
            Method: 'Delete',
            Response: 'openingId'
            Input: openingId
        """
        try:
            opening_id = request.query_params.get('opening_id')
            queryset = Opening.objects.get(opening_id=opening_id)

            total_qty = queryset.total_qty
            convertion_value = queryset.convertion_value
            stock_id = queryset.stock_id
            query_set = stock.objects.get(stock_id=stock_id)
            totalQty = convertion_value * total_qty
            sub_ttl = query_set.total_qty - total_qty
            sub_stk =  query_set.stock_qty - total_qty
            member = stock.objects.get(stock_id=stock_id)
            member.total_qty = sub_ttl
            member.stock_qty = sub_stk
            member.save()
            queryset.delete()
            error = {'status': status.HTTP_200_OK,'message': 'Stock Opening Deleted successfully'}
            return Response(data={'message':'Deleted Sucessfully'}, status=status.HTTP_200_OK)
        
        except RestrictedError:
            error = {'status': status.HTTP_400_BAD_REQUEST,'message': 'Stock Opening is being referenced with another instance'}
            return Response(data={'message':  "Stock Opening is being referenced with another instance"}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)

# Stock Opening Datatable
class StockOpeningDataTableAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
   
    def get(self, request):

        try:
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            product_id = request.query_params.get('product_id')

            queryset = Opening.objects.all()

            if product_id and product_id != "0":
                queryset = queryset.filter(product=product_id)

            if start_date and end_date:
                queryset = queryset.filter(created_at__date__range=[start_date, end_date])


            data_table = json.loads(request.GET.get('data_table', '{}'))

            data_table = json.loads(request.GET.get('data_table'))
            serializer_class = StockOpeningDatatableSerializer

            searchField = ['opening_id','product__product_name','batch_no','expire_date','total_qty','sales_amount','created_by','created_at']
            columns = ['opening_id','product__product_name','batch_no','expire_date','total_qty','sales_amount','created_by','created_at']

            context = {'request': request}

            result = datatable.DataTablesServer(request=data_table, columns=columns, qs=queryset, context=context,
                                                searchField=searchField, serializer=serializer_class).output_result()
            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)
        
# Post purchase invoice
class PurchaseApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = PostPurchaseSerializer(data=request.data)
            if serializer.is_valid():
                with transaction.atomic():
                    # Save the purchase and generate the purchase number
                    purchase_instance = serializer.save(purchase_no=code_generating('PUR'))
                    code_update('PUR')  # Update the code as necessary
                    purchase_id = purchase_instance.purchase_id

                    # Parse item details from the request
                    item_details = json.loads(request.data.get('itemdetail', '[]'))

                    for item in item_details:
                        batch_no = item.get('batchNo')
                        qty = int(item.get('qty'))
                        product = item.get('productId')
                        unit = item.get('unitId')
                        convertion_value = int(item.get('convertionValue'))
                        sales_amount = item.get('salesAmount')
                        mrp_amount = item.get('MRPAmount')
                        total_amount = item.get('totalAmount')

                        # Handle stock update or creation
                        stock_instance = stock.objects.filter(batch_no=batch_no, product=product).first()

                        # Create purchase detail record
                        purchasedet = PurchaseDet.objects.create(
                            purchase_id=purchase_id,
                            product_id=product,
                            unit_id=unit,
                            convertion_value=convertion_value,
                            batch_no=batch_no,
                            qty=qty,
                            mrp_amount=mrp_amount,
                            sales_amount=sales_amount,
                            total_amount=total_amount,
                            expire_date = stock_instance.expire_date,
                            stock_id = stock_instance.stock_id
                        )

                        total_qty = qty * convertion_value
                        unit_sales_amount = unitamountcalucaltion(sales_amount, convertion_value)

                       
                        if stock_instance:
                            if stock_instance.stock_qty < total_qty:
                                raise ValueError('This product has low stock. Please update stock!')
                            else:
                                stock_instance.stock_qty -= total_qty
                                stock_instance.save()
                        else:
                            stock_instance = stock.objects.create(
                                batch_no=batch_no,
                                product=product,
                                stock_qty=total_qty,
                                total_qty=total_qty,
                                unit=unit,
                                sales_amount=sales_amount,
                                unit_sales_amount=unit_sales_amount,
                            )

                        purchasedet.stock_id = stock_instance.stock_id
                        purchasedet.save()

                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return error_response.serializer_error(self.__class__.__name__, request, serializer)

        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)

# GEt purchase Details invoice      
class PurchaseDetDetailAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        try:
            purchase_id = request.query_params.get('purchase_id')
            queryset= getAllObjectWithFilter(PurchaseDet,{'purchase':purchase_id})
            serializer_class = PurchaseDetSerializer(queryset, many=True)
            return Response(serializer_class.data,status=status.HTTP_200_OK)
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)

# Put purchase invoice    
class UpdatePurchaseAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
           
            purchase_id = request.query_params.get('purchase_id')
            queryset = getObject(Purchase,{'purchase_id':purchase_id})
            context = {'purchase_id': purchase_id,'request': request}
            serializer_class = PostPurchaseSerializer(queryset, data=request.data, context=context, partial=True)

            if serializer_class.is_valid():
                with transaction.atomic():
                    serializer_class.save()  
                    existing_data = PurchaseDet.objects.filter(purchase=purchase_id)

                    for data in existing_data:
                        stock_id = data.stock_id
                        quantity = data.qty
                        convertion_value = data.convertion_value
                        totalqty = quantity * convertion_value
                        stock.objects.filter(stock_id=stock_id).update(stock_qty = F('stock_qty') + totalqty)
                    
                    existing_data.delete()
                    json_string = str(request.data.get('itemdetail'))
                    list_dicts = json.loads(json_string)

                    for itemdetail in list_dicts:
                        batch_no = itemdetail.get('batchNo')
                        qty = int(itemdetail.get('qty'))
                        product = itemdetail.get('productId')
                        unit = itemdetail.get('unitId')
                        convertion_value = int(itemdetail.get('convertionValue'))
                        sales_amount = itemdetail.get('salesAmount')
                        mrp_amount = itemdetail.get('MRPAmount')
                        total_amount = itemdetail.get('totalAmount')

                        # Handle stock update or creation
                        stock_instance = stock.objects.filter(batch_no=batch_no, product=product).first()
                        purchasedet = PurchaseDet.objects.create(
                            purchase_id = purchase_id,
                            product_id = product,
                            unit_id = unit, 
                            convertion_value = convertion_value,
                            batch_no = batch_no,
                            qty = qty,
                            mrp_amount = mrp_amount,
                            sales_amount = sales_amount,
                            total_amount = total_amount,
                            expire_date = stock_instance.expire_date,
                            stock_id = stock_instance.stock_id
                        )
                        total_qty = qty * convertion_value
                        unit_sales_amount = unitamountcalucaltion(sales_amount,convertion_value)

                        if stock_instance:
                            if stock_instance.stock_qty < total_qty:
                                raise ValueError('This product has low stock. Please update stock!')
                            else:
                                stock_instance.stock_qty -= total_qty
                                stock_instance.save()              
                        else:
                            raise ValueError('This product against batch no is mismatch')
                    return Response(serializer_class.data,status=status.HTTP_200_OK)
            else:
                return error_response.serializer_error(self.__class__.__name__, request, serializer_class)
        
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)     

    def get(self, request):
        """
            Summary or Description of the Function:
                * Get an Purchase details By ID.

            Parameters:
               purchaseId

            Method: 'GET',
            Response: 'JsonResponse'
            Input: 
            Output:{
                
            }
        """
      
        try:
            purchase_id = request.query_params.get('purchase_id')
            queryset = Purchase.objects.prefetch_related('tpdpurchaseid').get(purchase_id=purchase_id)
            serializer_class = GetTransPurchaseDetailsSerializers(queryset)
            return Response(serializer_class.data,status=status.HTTP_200_OK)

        except Exception as e:
             return error_response.exception_error(self.__class__.__name__, request, e)     
        
        
    def delete(self, request):
        
        try:
            purchase_id = request.query_params.get('purchase_id')
            purchaseDet =  getAllObjectWithFilter(PurchaseDet,{'purchase':purchase_id})
            purchase = getAllObjectWithFilter(Purchase,{'purchase_id':purchase_id})
            with transaction.atomic():
                existing_data = getAllObjectWithFilter(PurchaseDet,{'purchase':purchase_id}) 

                for data in existing_data:
                    stock_id = data.stock_id
                    qty = data.qty 
                    convertion_value = data.convertion_value
                    tot_qty = qty * convertion_value      

                    stock.objects.filter(stock_id=stock_id).update(stock_qty=F('stock_qty') + tot_qty)
                    stockQty = stock.objects.get(stock_id=stock_id).stock_qty
                    if stockQty < 0:
                        raise ValueError('Low Stock Quaility')
                purchaseDet.delete()
                purchase.delete()
                return Response(data=CommonApiMessages.delete('Purchase Invoice'), status=status.HTTP_200_OK)

        except RestrictedError:
            return Response(data=CommonApiMessages.restrict_delete('Purchase Invoice'), status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e) 
        
# purchase invoice Datatable
class PurchaseDatatableAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):

        try:
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')

            queryset = Purchase.objects.select_related('bill_type').prefetch_related('tpdpurchaseid__stock').filter(purchase_date__date__range=[start_date,end_date])
            data_table = json.loads(request.GET.get('data_table'))

            serializer_class = GetPurchaseSerializer
            searchField = ['purchase_no','purchase_date','net_amount','bill_type__bill_type']
            columns = ['purchase_no','purchase_date','net_amount','bill_type__bill_type']
                    
            context = {'request': request}
            result = datatable.DataTablesServer(request=data_table, columns=columns, qs=queryset, context=context,
                                                searchField=searchField, serializer=serializer_class).output_result()
            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
           return error_response.exception_error(self.__class__.__name__, request, e) 

# Stock Datatable     
class StockDatatableAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            product_id = request.query_params.get('product_id')
            stock_id = request.query_params.get('stock_id')

            # Initialize the queryset
            queryset = stock.objects.all()

            # Apply filters based on provided parameters
            if product_id and product_id != "0":
                queryset = queryset.filter(product=product_id)

            if start_date and end_date:
                queryset = queryset.filter(created_at__date__range=[start_date, end_date])

            if stock_id:
                queryset = queryset.filter(stock_id=stock_id)

            data_table = json.loads(request.GET.get('data_table', '{}'))

            serializer_class = StockDtSerializer
            search_fields = ['stock_id', 'batch_no', 'expire_date', 'stock_qty', 'total_qty']
            columns = ['stock_id', 'batch_no', 'expire_date', 'stock_qty', 'total_qty']
                    
            context = {'request': request}
            result = datatable.DataTablesServer(
                request=data_table,
                columns=columns,
                qs=queryset,
                context=context,
                searchField=search_fields,
                serializer=serializer_class
            ).output_result()

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)


# BATCH AND product against Stock ::     
class GetAvailableStockAgainstBatchAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            batch_no = request.query_params.get('batch_no')
            product_id = request.query_params.get('product_id')
            query_set = getAllObjectWithFilter(stock, {"batch_no": batch_no,"product_id":product_id})
            data = {
                'stock_qty': list(query_set.values_list('stock_qty', flat=True))
            }
            return Response(data=data, status=status.HTTP_200_OK)

        except Exception as e:
           return error_response.exception_error(self.__class__.__name__, request, e) 
        
# CASCADING FOR PRODUCT AGAINST BATCH NO
class GetProductAgainstBatchAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            product_id = request.query_params.get("product_id", '')
            if product_id != '':
                query_set = list(getAllObjectWithFilter(stock,{'product':product_id}).values("batch_no", "product","stock_qty","stock_id").order_by("stock_id"))
            else:
                query_set = {}
            return Response(query_set, status=status.HTTP_200_OK)

        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e) 
        
# Post POS
class CreatePOSApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = PostPosSerializer(data=request.data)
            if serializer.is_valid():
                with transaction.atomic():
                    # Save the pos and generate the pos number
                    pos_instance = serializer.save(pos_no=code_generating('INV'))
                    code_update('INV')  # Update the code as necessary
                    pos_id = pos_instance.pos_id

                    # Parse item details from the request
                    item_details = json.loads(request.data.get('itemdetail', '[]'))

                    for item in item_details:
                        categoryId = item.get('categoryId')
                        actWeight = item.get('actWeight')
                        avgWeight = item.get('avgWeight')
                        totalAmount = item.get('totalAmount')
                    
                        # Create pos detail record
                        purchasedet = PosDet.objects.create(
                            pos_id=pos_id,
                            category_id=categoryId,
                            actual_wgt=actWeight,
                            avg_wgt=avgWeight,
                            total_amount=totalAmount,
                        )
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return error_response.serializer_error(self.__class__.__name__, request, serializer)

        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)
        
# GEt POS Details invoice      
class PosDetDetailAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        try:
            pos_id = request.query_params.get('pos_id')
            queryset= getAllObjectWithFilter(PosDet,{'pos':pos_id})
            serializer_class = PosDetSerializer(queryset, many=True)
            return Response(serializer_class.data,status=status.HTTP_200_OK)
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)
        
# Put POS  
class UpdatePosAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
           
            pos_id = request.query_params.get('pos_id')
            queryset = getObject(POS,{'pos_id':pos_id})
            context = {'pos_id': pos_id,'request': request}
            serializer_class = PostPosSerializer(queryset, data=request.data, context=context, partial=True)

            if serializer_class.is_valid():
                with transaction.atomic():
                    serializer_class.save()  
                    existing_data = PosDet.objects.filter(pos=pos_id).delete()

                    json_string = str(request.data.get('itemdetail'))
                    list_dicts = json.loads(json_string)

                    for item in list_dicts:
                        categoryId = item.get('categoryId')
                        actWeight = item.get('actWeight')
                        avgWeight = item.get('avgWeight')
                        totalAmount = item.get('totalAmount')
                    
                        # Create pos detail record
                        purchasedet = PosDet.objects.create(
                            pos_id=pos_id,
                            category_id=categoryId,
                            actual_wgt=actWeight,
                            avg_wgt=avgWeight,
                            total_amount=totalAmount,
                        )
                    return Response(serializer_class.data,status=status.HTTP_200_OK)
            else:
                return error_response.serializer_error(self.__class__.__name__, request, serializer_class)
        
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)     

    def get(self, request):
        
        try:
            pos_id = request.query_params.get('pos_id')
            queryset = POS.objects.prefetch_related('tpdposid').get(pos_id=pos_id)
            serializer_class = GetPosDetailsSerializers(queryset)
            return Response(serializer_class.data,status=status.HTTP_200_OK)

        except Exception as e:
             return error_response.exception_error(self.__class__.__name__, request, e)     
        
    def delete(self, request):
        
        try:
            pos_id = request.query_params.get('pos_id')
            posDet =  getAllObjectWithFilter(PosDet,{'pos':pos_id})
            pos = getAllObjectWithFilter(POS,{'pos_id':pos_id})

            with transaction.atomic():
                posDet.delete()
                pos.delete()
                return Response(data=CommonApiMessages.delete('POS'), status=status.HTTP_200_OK)

        except RestrictedError:
            return Response(data=CommonApiMessages.restrict_delete('POS'), status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e) 
        
# pos Datatable
class PosDatatableAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):

        try:
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            queryset = POS.objects.select_related('bill_type').filter(pos_date__date__range=[start_date,end_date])
            data_table = json.loads(request.GET.get('data_table'))

            serializer_class = PosDtSerializer
            searchField = ['pos_no','pos_date','net_amount','bill_type__bill_type']
            columns = ['pos_no','pos_date','net_amount','bill_type__bill_type']
                    
            context = {'request': request}
            result = datatable.DataTablesServer(request=data_table, columns=columns, qs=queryset, context=context,
                                                searchField=searchField, serializer=serializer_class).output_result()
            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
           return error_response.exception_error(self.__class__.__name__, request, e) 
