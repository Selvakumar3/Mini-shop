from rest_framework.views import APIView
from flourishapi.serializers.settings import *
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

class BillnosettingsAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            query_set = getFirstObject(BillnoSettings)
            serializer_class = BillSettingsSerializer(query_set)
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e) 
    
    def post(self,request):
        try:
            if BillnoSettings.objects.exists():
                queryset = getFirstObject(BillnoSettings)
                serializer_class = BillSettingsSerializer(queryset,data = request.data,partial=True)
                if serializer_class.is_valid():
                    serializer_class.save()          
                    return Response(serializer_class.data,status=status.HTTP_200_OK)
                else:
                    return error_response.serializer_error(self.__class__.__name__, request, serializer_class)
            else:
                serializer_class = BillSettingsSerializer(data = request.data)
                if serializer_class.is_valid():
                    serializer_class.save()          
                    return Response(serializer_class.data,status=status.HTTP_201_CREATED)
                else:
                    return error_response.serializer_error(self.__class__.__name__, request, serializer_class)
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)
        

# Admin Settings ::
class AdminSettingsAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            query_set = getFirstObject(AdminSettings)
            serializer_class = AdminSettingsSerializer(query_set, context={'request': request})
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)
        
    def post(self,request):
        try:
            if AdminSettings.objects.all().exists():
                queryset = getFirstObject(AdminSettings)
                serializer_class = AdminSettingsSerializer(queryset,data = request.data,partial=True)
                if serializer_class.is_valid():
                    serializer_class.save()          
                    return Response(serializer_class.data,status=status.HTTP_200_OK)
                else:
                    return error_response.serializer_error(self.__class__.__name__, request, serializer_class)
            else:
                serializer_class = AdminSettingsSerializer(data = request.data)
                if serializer_class.is_valid():
                    serializer_class.save()          
                    return Response(serializer_class.data,status=status.HTTP_201_CREATED)
                else:
                    return error_response.serializer_error(self.__class__.__name__, request, serializer_class)
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)
        
# Email Settings ::
class EmailSettingsAPI(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):

        try:
            query_set = getFirstObject(EmailSettings)
            serializer_class = EmailSettingsSerializer(query_set)
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)

    
    def post(self,request):
        try:
            
            if EmailSettings.objects.exists():

                queryset = getFirstObject(EmailSettings)
                serializer_class = EmailSettingsSerializer(queryset,data = request.data,partial=True)
                if serializer_class.is_valid():
                    serializer_class.save()          
                    return Response(serializer_class.data,status=status.HTTP_200_OK)
                else:
                    return error_response.serializer_error(self.__class__.__name__, request, serializer_class)
            else:

                serializer_class = EmailSettingsSerializer(data = request.data)
                if serializer_class.is_valid():
                    serializer_class.save()          
                    return Response(serializer_class.data,status=status.HTTP_201_CREATED)
                else:
                    return error_response.serializer_error(self.__class__.__name__, request, serializer_class)
                
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)


  

        