# third-party
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from flourishapi.models import *
from flourishapi import datatable
from datetime import datetime
import traceback
from flourishapi.serializers.common import *
from django.db.models import F, Sum, Prefetch
from flourishapi.utils import * 
from django.db.models import RestrictedError
from django.db import transaction
import json
import jwt
from flourishapi import datatable
# Log functions ::
class LogAPI(generics.ListCreateAPIView):
    queryset = Logs.objects.all()
    serializer_class = LogSerializer

class LogReportAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Summary or Description of the Function:
            * Get Log Reports.
        """
        try:
            # Retrieve query parameters
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            log_type = request.query_params.get('type')

            # Initialize the queryset
            queryset = Logs.objects.all()

            # Filter based on log type and date range
            if start_date and end_date:
                queryset = queryset.filter(log_date__date__range=[start_date, end_date])
                
                if log_type == 'Web':
                    queryset = queryset.filter(log_type=log_type)
                elif log_type == 'API':
                    queryset = queryset.exclude(log_type='Web')
            
            # Get data for DataTables
            data_table = json.loads(request.GET.get('data_table'))
            serializer_class = GetLogReportsSerializer  

            search_field = ["log_id", "transaction_name", "mode", "Ip_address", "system_name", "log_date", "log_type", "log_message"]
            columns = ["-log_id", "transaction_name", "mode", "Ip_address", "system_name", "log_date", "log_type", "log_message"]
            context = {'request': request}

            # Process the DataTable request
            result = datatable.DataTablesServer(request=data_table, columns=columns, qs=queryset, context=context,
                                                searchField=search_field, serializer=serializer_class).output_result()
            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)

# Menu Functions ::
class getallmenuApi(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_id = request.query_params.get('user_id')
            userData = getObject(User,{'id':user_id})
            groupId = userData.usergroup_id

            if getAllObjectWithFilter(User,{'id':user_id,'is_super_admin':True, 'is_active':True}).exists():
                queryset = getAllObjectWithFilter(Menu,{'is_visible':True}).order_by('row_index').exclude(menu_id=1)

            elif getAllObjectWithFilter(User,{'id':user_id,'is_active':True}).exists():
                menuIds = getAllObjectWithFilter(UserGroupMenu,{'usergroup_id':groupId}).values_list('menu_id', flat=True)
                queryset = getAllObjectWithFilter(Menu,{'menu_id__in':menuIds,'is_visible':True}).order_by('row_index').exclude(menu_id=1)
            else:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            serialized_data = menuDetailsSerializers(queryset, many=True)
            return Response(serialized_data.data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)
        
# GET Usergroup fuunctions ::
class UserGroupMenuApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            query_set = getAllObject(UserGroup)
            serializer_class = UserGroupListMenuSerializers(query_set, many=True)
            return Response(serializer_class.data, status=status.HTTP_202_ACCEPTED)
        
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)
        
# GET USERGROUP MENU LIST ::
class UserGroupMenuListApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_id = request.query_params.get('user_id')

            if user_id is None or user_id == "":
                return Response({'Message': "user_id field is required"}, status=status.HTTP_400_BAD_REQUEST)

            userData = getObject(User,{'id':user_id})
            groupId = userData.usergroup

            if userData.is_super_admin:
                queryset = getAllObject(Menu).order_by('row_index', 'menu_id')
                
            elif getAllObjectWithFilter(User,{'id':user_id,'is_admin':True,'is_active':True}).exists():
                menuIds = getAllObjectWithFilter(UserGroupMenu,{'usergroup_id':groupId}).values_list('menu_id', flat=True)
                queryset = getAllObjectWithFilter(Menu,{'menu_id__in':menuIds})
            else:
                return Response({'Message': "Invalid user_id or insufficient privileges"}, status=status.HTTP_403_FORBIDDEN)

            serialized_data = UserMenuSerializers(queryset, many=True).data
            return Response(serialized_data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'Message': "Invalid user_id"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)

    def post(self, request):

        try:
            serializer_class = PostUserGroupMenuSerializers(data=request.data)
            if serializer_class.is_valid():

                with transaction.atomic():
                    serializer_class.save()
                    usergroup_id = serializer_class.data.get('usergroup_id')
                    menu_id = json.loads(request.data.get('menuIdDet'))
                    for menu in menu_id:
                        UserGroupMenu.objects.create(
                            usergroup_id=usergroup_id, menu_id=menu['menu_id'])
                        
                    error = {'message': 'Usergroup created successfully'}
                    return Response(serializer_class.data, status=status.HTTP_201_CREATED)
            else:
                return error_response.serializer_error(self.__class__.__name__, request, serializer_class)

        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)
        

# Usergroup List function ::
class GetUserGroupListAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
       
        try:
            queryset = getAllObject(UserGroup).order_by('usergroup_id')
            serializer_class = UserGroupListMenuSerializers(queryset, many=True)
            return Response(serializer_class.data, status=status.HTTP_200_OK)

        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)
        

# UPDATE AND DELETE FUNCTION::
class UpdateUserGroupMenuAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
      
        user_id = request.query_params.get('user_id')
        try:

            usergroup_id = request.query_params.get('usergroup_id')
            context={'usergroup_id':usergroup_id}

            queryset = getObject(UserGroup,{'usergroup_id':usergroup_id})
            serializer_class = PostUserGroupMenuSerializers(queryset,data=request.data,context=context)
            if serializer_class.is_valid():
                with transaction.atomic():    # rollback all saved data if any error occurs
                    serializer_class.save()
                    usergroup_id = serializer_class.data.get('usergroup_id')
                    
                    # convert json string to python dictonary
                    menu_id = json.loads(request.data.get('menuIdDet'))
                    
                    # delete and create usergroup menu    
                    getAllObjectWithFilter(UserGroupMenu,{'usergroup_id':usergroup_id}).delete()
                    
                    # create  masUserGroupMenu by UserGroupID
                    for menu in menu_id:

                        UserGroupMenu.objects.create(usergroup_id=usergroup_id, menu_id=menu['menu_id'])
                    msg = {'status': status.HTTP_202_ACCEPTED,'message': "UserGroup updated successfully"}
                    return Response(serializer_class.data, status=status.HTTP_200_OK)
                
            else:
                return error_response.serializer_error(self.__class__.__name__, request, serializer_class)

        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)
        
    def delete(self, request):
        
        try:
            usergroup_id = request.query_params.get('usergroup_id')

            queryset = getAllObjectWithFilter(UserGroupMenu,{'usergroup_id':usergroup_id}).delete()
            queryset = getAllObjectWithFilter(UserGroup,{'usergroup_id':usergroup_id}).delete()
            msg = {'status':status.HTTP_200_OK,'message': 'Usergroup deleted successfully'}
            return Response(data={"message":"UserGroup Deleted Successfully"}, status=status.HTTP_202_ACCEPTED)
        
        except RestrictedError:
                msg = {'status':status.HTTP_400_BAD_REQUEST,'message': 'Usergroup deleted failed'}
                return Response(data={'message':  "UserGroup is being Referenced with another instance"}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)
        
# Usergroup Datatables FUNCTION::
class GetUserdatatableAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_group_list = getAllObject(UserGroup)

            data_table = json.loads(request.GET.get('data_table'))
            serializer_class = UserGroupListMenuSerializers

            searchField =['usergroup_id','usergroup_name']
            columns = ['usergroup_id','usergroup_name']

            result = datatable.DataTablesServer(request=data_table, columns=columns, qs=user_group_list,
            searchField=searchField,serializer=serializer_class).output_result()
            return Response(result, status.HTTP_200_OK)

        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)


# Generate Code ::
class GetGenerateCodeApi(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        try:
            codetype = request.query_params.get('codetype')
            code = code_generating(codetype)
            return Response({'code':code},status=status.HTTP_200_OK)
        
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)
        

# Get Billtype ::
class GetBillTypeAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
            Summary or Description of the function:
                Get all bill type Data from Database.
        """
        try:
            query_set =  getAllObjectWithFilter(BillType).values('bill_typeid','bill_type')
            return Response(data=query_set, status=status.HTTP_200_OK)
        
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)


# DASHBOARD STOCK DETAIL
class DashboardViewApi(APIView):
    def get(self, request):
    
        # Querysets for today, total, and expired stocks
        today_stock = stock.objects.filter(created_at__date=date_only) 
        total_stock = stock.objects.filter(expire_date__gte=date_only) 
        expired_stock = stock.objects.filter(expire_date__lt=date_only) 

        # Aggregate quantities
        today_qty = today_stock.aggregate(total_qty=Sum('total_qty'))['total_qty'] or 0
        total_qty = total_stock.aggregate(total_qty=Sum('total_qty'))['total_qty'] or 0
        expired_qty = expired_stock.aggregate(expired_qty=Sum('total_qty'))['expired_qty'] or 0
        
        # Return response
        return Response({
            'today_qty': today_qty,
            'expired_qty': expired_qty,
            'total_qty': total_qty
        }, status=status.HTTP_200_OK)
    

from collections import defaultdict
from datetime import datetime, timedelta
import pytz
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal

kolkata_tz = pytz.timezone('Asia/Kolkata')

class WeeklyNetAmountView(APIView):
    def get(self, request):
        try:
            today = datetime.now(kolkata_tz)
            start_of_week = today - timedelta(days=today.weekday())  # Monday of this week
            start_of_last_week = start_of_week - timedelta(days=7)  # Monday of last week
            end_of_last_week = start_of_week - timedelta(days=1)  # Sunday of last week

            # Initialize dictionaries to hold sums
            current_week_data = defaultdict(Decimal)  # Use Decimal instead of float
            last_week_data = defaultdict(Decimal)     # Use Decimal instead of float

            # Query purchases for the last week
            last_week_purchases = Purchase.objects.filter(created_at__date__range=[start_of_last_week, end_of_last_week])
            for purchase in last_week_purchases:
                day = purchase.created_at.strftime('%a').lower()  # Get the day name (mon, tue, ...)
                last_week_data[day] += Decimal(purchase.net_amount)  # Convert to Decimal

            # Query purchases for the current week
            current_week_purchases = Purchase.objects.filter(created_at__date__range=[start_of_week, today])
            for purchase in current_week_purchases:
                day = purchase.created_at.strftime('%a').lower()  # Get the day name (mon, tue, ...)
                current_week_data[day] += Decimal(purchase.net_amount)  # Convert to Decimal

            # Format the result into the desired structure
            days_of_week = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
            last_week_result = [{day: float(last_week_data[day])} for day in days_of_week]  # Convert back to float for response
            current_week_result = [{day: float(current_week_data[day])} for day in days_of_week]  # Convert back to float for response

            return Response({
                'last_week': last_week_result,
                'current_week': current_week_result
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print('======Error============', e)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
