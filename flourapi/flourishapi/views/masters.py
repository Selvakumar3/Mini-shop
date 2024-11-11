from rest_framework.views import APIView
from flourishapi.serializers.masters import *
from flourishapi.serializers.user import *
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
from django.contrib.auth.hashers import make_password

# GET AND POST Category FUNCTION ::
class CreateCategoryAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
            Summary or Description of the function:
                Get all Category Data from Database.
        """
        try:
            query_set =  getAllObjectWithFilter(Category,{'is_active':True}).order_by('categoryid')
            serializer_class = GetCategorySerializer(query_set, many=True)
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)

    def post(self, request):
        """
        Summary or Description of the function:
            Post Category data to database.
        """
        try:
            serializer_class = PostCategorySerializer(data=request.data)
            if serializer_class.is_valid():
                serializer_class.save()
                return Response(serializer_class.data, status=status.HTTP_201_CREATED)
            else:
                return error_response.serializer_error(self.__class__.__name__, request, serializer_class)
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)


# UPDATE, DELETE Category FUNCTION ::
class CategoryUpdateAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Summary or Description of the function:
            Get particular category by using Category_id from Database.
        """
        try:
            category_id = request.query_params.get('category_id')
            query_set = getObject(Category,{'categoryid':category_id})
            serializer_class = PostCategorySerializer(query_set, context={'request':request})
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return error_response.serializer_error(self.__class__.__name__, request, serializer_class)
                         
    def put(self, request):
        """
        Summary or Description of the function:
            Put particular category by using category_id from Database.
        """

        try:
            category_id = request.query_params.get('category_id')
            query_set = getObject(Category,{'categoryid':category_id})
            serializer_class = PostCategorySerializer(query_set, data=request.data,context={'category_id':category_id})

            if serializer_class.is_valid():
                serializer_class.save()
                return Response(serializer_class.data, status=status.HTTP_200_OK)
            else:
                return error_response.serializer_error(self.__class__.__name__, request, serializer_class)
        except Exception as e:
           return error_response.exception_error(self.__class__.__name__, request, e)
                
    def delete(self, request):
        """
            Summary or Description of the Function:
                * Delete an Category By ID.
        """
        try:
            category_id = request.query_params.get('category_id')
            getAllObjectWithFilter(Category,{'categoryid':category_id}).delete()
            return Response(data=CommonApiMessages.delete('Category'), status=status.HTTP_200_OK)
        
        except RestrictedError:
            return Response(data=CommonApiMessages.restrict_delete('Category'), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e) 


# Category DATATABLES ::
class CategoryDataTableAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Summary or Description of the function:
            Get all Category from Database with datatable format.
        """
        try:
            queryset = getAllObject(Category).order_by('categoryid')
            data_table = json.loads(request.GET.get('data_table'))
            serializer_class = GetCategorySerializer

            searchField =  ['categoryid','category_name', 'category_desc','is_active']
            columns = ['categoryid','category_image','category_name', 'category_desc','is_active']
            context = {'request': request}

            result = datatable.DataTablesServer(request=data_table, columns=columns, qs=queryset, context=context,
                                                searchField=searchField, serializer=serializer_class).output_result()
            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)
        
# Update Status For Category
class updateStausForCategoryApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        """
            Summary or Description of the Function:
                * Update Active For Category By ID.
        """
        try:
            category_id = request.query_params.get('category_id')
            is_active = request.query_params.get('is_active')
            getAllObjectWithFilter(Category,{'categoryid': category_id}).update(is_active= False if (is_active == '0' or 0) else True)
            return Response(data=CommonApiMessages.update_status('Category'),status=status.HTTP_200_OK)
        
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)
        
# GET AND POST Brand FUNCTION ::
class CreateBrandAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
            Summary or Description of the function:
                Get all Brand Data from Database.
        """
        try:
            query_set =  getAllObjectWithFilter(Brand,{'is_active':True}).order_by('brand_id')
            serializer_class = GetBrandSerializer(query_set, many=True)
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)

    def post(self, request):
        """
        Summary or Description of the function:
            Post Brand data to database.
        """
        try:
            serializer_class = PostBrandSerializer(data=request.data)
            if serializer_class.is_valid():
                serializer_class.save()
                return Response(serializer_class.data, status=status.HTTP_201_CREATED)
            else:
                return error_response.serializer_error(self.__class__.__name__, request, serializer_class)
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)
        
# UPDATE, DELETE Brand FUNCTION ::
class BrandUpdateAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Summary or Description of the function:
            Get particular Brand by using Brand_id from Database.
        """
        try:
            brand_id = request.query_params.get('brand_id')
            query_set = getObject(Brand,{'brand_id':brand_id})
            serializer_class = PostBrandSerializer(query_set, context={'request':request})
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return error_response.serializer_error(self.__class__.__name__, request, serializer_class)
                         
    def put(self, request):
        """
        Summary or Description of the function:
            Put particular brand by using brand_id from Database.
        """

        try:
            brand_id = request.query_params.get('brand_id')
            query_set = getObject(Brand,{'brand_id':brand_id})
            serializer_class = PostBrandSerializer(query_set, data=request.data,context={'brand_id':brand_id})

            if serializer_class.is_valid():
                serializer_class.save()
                return Response(serializer_class.data, status=status.HTTP_200_OK)
            else:
                return error_response.serializer_error(self.__class__.__name__, request, serializer_class)
        except Exception as e:
           return error_response.exception_error(self.__class__.__name__, request, e)
                

    def delete(self, request):
        """
            Summary or Description of the Function:
                * Delete an Brand By ID.
        """
        try:
            brand_id = request.query_params.get('brand_id')

            getAllObjectWithFilter(Brand,{'brand_id':brand_id}).delete()
            return Response(data=CommonApiMessages.delete('Brand'), status=status.HTTP_200_OK)
        
        except RestrictedError:
            return Response(data=CommonApiMessages.restrict_delete('Brand'), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e) 
        
# Brand DATATABLES ::
class BrandDataTableAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Summary or Description of the function:
            Get all Brand from Database with datatable format.
        """
        try:
            queryset = getAllObject(Brand).order_by('brand_id')
            data_table = json.loads(request.GET.get('data_table'))

            serializer_class = GetBrandDtSerializer

            searchField =  ['brand_id','brand_name','is_active','category__category_name']

            columns =  ['brand_id','brand_name','is_active','category__category_name']

            context = {'request': request}

            result = datatable.DataTablesServer(request=data_table, columns=columns, qs=queryset, context=context,
                                                searchField=searchField, serializer=serializer_class).output_result()
            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)
        
# Update Status For brand
class updateStausForbrandApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        """
            Summary or Description of the Function:
                * Update Active For brand By ID.
        """
        try:
            brand_id = request.query_params.get('brand_id')
            is_active = request.query_params.get('is_active')

            getAllObjectWithFilter(Brand,{'brand_id': brand_id}).update(is_active= False if (is_active == '0' or 0) else True)
            return Response(data=CommonApiMessages.update_status('Brand'),status=status.HTTP_200_OK)
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)
        

# GET AND POST Unit FUNCTION ::
class CreateUnitAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
            Summary or Description of the function:
                Get all Unit Data from Database.
        """
        try:
            query_set =  getAllObjectWithFilter(Unit,{'is_active':True}).order_by('unit_id')
            serializer_class = GetUnitSerializer(query_set, many=True)
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)

    def post(self, request):
        """
        Summary or Description of the function:
            Post Unit data to database.
        """
        try:
            serializer_class = PostUnitSerializer(data=request.data)
            if serializer_class.is_valid():
                serializer_class.save()
                return Response(serializer_class.data, status=status.HTTP_201_CREATED)
            else:
                return error_response.serializer_error(self.__class__.__name__, request, serializer_class)
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)
        
# UPDATE, DELETE Unit FUNCTION ::
class UnitUpdateAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Summary or Description of the function:
            Get particular Unit by using Unit_id from Database.
        """
        try:
            unit_id = request.query_params.get('unit_id')
            query_set = getObject(Unit,{'unit_id':unit_id})
            serializer_class = PostUnitSerializer(query_set, context={'request':request})
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return error_response.serializer_error(self.__class__.__name__, request, serializer_class)
                         
    def put(self, request):
        """
        Summary or Description of the function:
            Put particular brand by using brand_id from Database.
        """

        try:
            unit_id = request.query_params.get('unit_id')
            query_set = getObject(Unit,{'unit_id':unit_id})
            serializer_class = PostUnitSerializer(query_set, data=request.data,context={'unit_id':unit_id})

            if serializer_class.is_valid():
                serializer_class.save()
                return Response(serializer_class.data, status=status.HTTP_200_OK)
            else:
                return error_response.serializer_error(self.__class__.__name__, request, serializer_class)
        except Exception as e:
           return error_response.exception_error(self.__class__.__name__, request, e)
                
    def delete(self, request):
        """
            Summary or Description of the Function:
                * Delete an Unit By ID.
        """
        try:
            unit_id = request.query_params.get('unit_id')

            getAllObjectWithFilter(Unit,{'unit_id':unit_id}).delete()
            return Response(data=CommonApiMessages.delete('Unit'), status=status.HTTP_200_OK)
        
        except RestrictedError:
            return Response(data=CommonApiMessages.restrict_delete('Unit'), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e) 
        
# Unit DATATABLES ::
class UnitDataTableAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Summary or Description of the function:
            Get all Unit from Database with datatable format.
        """
        try:
            queryset = getAllObject(Unit).order_by('unit_id')
            data_table = json.loads(request.GET.get('data_table'))

            serializer_class = GetUnitSerializer

            searchField =  ['unit_id','unit_name']

            columns =  ['unit_id','unit_name']

            context = {'request': request}

            result = datatable.DataTablesServer(request=data_table, columns=columns, qs=queryset, context=context,
                                                searchField=searchField, serializer=serializer_class).output_result()
            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)
        
# GET AND POST Product FUNCTION ::
class CreateProductAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
            Summary or Description of the function:
                Get all Product Data from Database.
        """
        try:
            query_set =  getAllObjectWithFilter(Product,{'is_active':True}).order_by('product_id')
            serializer_class = GetProductSerializer(query_set, many=True)
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)

    def post(self, request):
        """
        Summary or Description of the function:
            Post Product data to database.
        """
        try:
            serializer_class = PostProductSerializer(data=request.data)
            if serializer_class.is_valid():
                serializer_class.save()
                return Response(serializer_class.data, status=status.HTTP_201_CREATED)
            else:
                return error_response.serializer_error(self.__class__.__name__, request, serializer_class)
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)
        
# UPDATE, DELETE Product FUNCTION ::
class ProductUpdateAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Summary or Description of the function:
            Get particular Product by using Product_id from Database.
        """
        try:
            product_id = request.query_params.get('product_id')
            query_set = getObject(Product,{'product_id':product_id})
            serializer_class = PostProductSerializer(query_set, context={'request':request})
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return error_response.serializer_error(self.__class__.__name__, request, serializer_class)
                         
    def put(self, request):
        """
        Summary or Description of the function:
            Put particular Product by using Product_id from Database.
        """

        try:
            product_id = request.query_params.get('product_id')
            query_set = getObject(Product,{'product_id':product_id})
            serializer_class = PostProductSerializer(query_set, data=request.data,context={'product_id':product_id})

            if serializer_class.is_valid():
                serializer_class.save()
                return Response(serializer_class.data, status=status.HTTP_200_OK)
            else:
                return error_response.serializer_error(self.__class__.__name__, request, serializer_class)
        except Exception as e:
           return error_response.exception_error(self.__class__.__name__, request, e)
                
    def delete(self, request):
        """
            Summary or Description of the Function:
                * Delete an Product By ID.
        """
        try:
            product_id = request.query_params.get('product_id')
            getAllObjectWithFilter(Product,{'product_id':product_id}).delete()
            return Response(data=CommonApiMessages.delete('Product'), status=status.HTTP_200_OK)
        
        except RestrictedError:
            return Response(data=CommonApiMessages.restrict_delete('Product'), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e) 
        
# Product DATATABLES ::
class ProductDataTableAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Summary or Description of the function:
            Get all Product from Database with datatable format.
        """
        try:
            queryset = getAllObject(Product).order_by('product_id')
            data_table = json.loads(request.GET.get('data_table'))
            serializer_class = GetProductDtSerializer

            searchField = [ "product_id","product_name","product_image","mrp","customer_price","is_active"]
            columns = [ "product_id","product_name","product_image","mrp","customer_price","is_active"]
            context = {'request': request}

            result = datatable.DataTablesServer(request=data_table, columns=columns, qs=queryset, context=context,
                                                searchField=searchField, serializer=serializer_class).output_result()
            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            print('dmkffksfds',e)
            return error_response.exception_error(self.__class__.__name__, request, e)

# Update Status For Product
class updateStausForProductApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        """
            Summary or Description of the Function:
                * Update Active For Product By ID.
        """
        try:
            product_id = request.query_params.get('product_id')
            is_active = request.query_params.get('is_active')
            getAllObjectWithFilter(Product,{'product_id': product_id}).update(is_active= False if (is_active == '0' or 0) else True)
            return Response(data=CommonApiMessages.update_status('Product'),status=status.HTTP_200_OK)
        
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)
        
# GET AND POST EMPLOYEE FUNCTION ::
class CreateEmployeeAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
            Summary or Description of the function:
                Get all Employee Data from Database.
        """
        try:
            query_set =  getAllObjectWithFilter(Employee,{'is_active':True}).order_by('employee_id')
            serializer_class = GetEmployeeSerializer(query_set, many=True)
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)

    
    def post(self, request):
        """
        Create a new employee record in the database.
        """
        try:
            employee_data = {
                'first_name': request.data.get('first_name'),
                'last_name': request.data.get('last_name'),
                'doj': request.data.get('doj'),
                'mobile_number': request.data.get('mobile_number'),
                'email': request.data.get('email'),
                'address': request.data.get('address'),
                'username': request.data.get('username'),
                'usergroup': request.data.get('usergroup'),
                'is_active': True,
                'created_by': request.data.get('created_by'),
                'password': request.data.get('password'),
            }

            # Generate display name
            employee_data['display_name'] = f"{employee_data['first_name']} {employee_data['last_name']}".strip()

            # Validate and save employee data
            employee_serializer = PostEmployeeSerializer(data=employee_data)
            if employee_serializer.is_valid():
                with transaction.atomic():
                    employee_serializer.save(employee_no=code_generating('EMP'))
                    code_update('EMP')
                    employee_id = employee_serializer.data.get('employee_id')
                    usergroup_id = employee_serializer.data.get('usergroup')

                  # Create associated user
                    user = User.objects.create(
                        username=employee_data['username'],
                        display_name=employee_data['display_name'],
                        mobile_number=employee_data['mobile_number'],
                        email=employee_data['email'],
                        password=make_password(employee_data['password']),
                        usergroup_id = usergroup_id
                    )
                    user_id = user.id
                    Employee.objects.filter(employee_id=employee_id).update(emp_user=user_id)

                return Response(employee_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return error_response.serializer_error(self.__class__.__name__, request, employee_serializer.errors)
            
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)
        
# UPDATE, DELETE Employee FUNCTION ::
class EmployeeUpdateAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Summary or Description of the function:
            Get particular Employee by using Employee_id from Database.
        """
        try:
            employee_id = request.query_params.get('employee_id')
            query_set = getObject(Employee,{'employee_id':employee_id})
            serializer_class = GetEmployeeSerializer(query_set, context={'request':request})
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return error_response.serializer_error(self.__class__.__name__, request, serializer_class)
                         
    def put(self, request):
        """
        Update a particular Employee using employee_id from the database.
        """

        try:
            employee_id = request.query_params.get('employee_id')
            pass_word = request.data.get('password')

            query_set = getObject(Employee, {'employee_id': employee_id})
            serializer_class = PostEmployeeSerializer(query_set, data=request.data, context={'employee_id': employee_id})

            if serializer_class.is_valid():
                with transaction.atomic():
                    serializer_class.save()
                    user_id = serializer_class.data.get('emp_user')
                    display_name = f"{serializer_class.data.get('first_name')} {serializer_class.data.get('last_name')}"
                    
                    # Update the corresponding User object
                    User.objects.filter(id=user_id).update(
                        username=serializer_class.data.get('username'),
                        display_name=display_name,
                        mobile_number=serializer_class.data.get('mobile_number'),
                        email=serializer_class.data.get('email'),
                        usergroup=serializer_class.data.get('usergroup')
                    )
                    
                    # Update the password if provided
                    if pass_word:
                        user = User.objects.get(id=user_id)
                        user.password = make_password(pass_word)
                        user.save()
                return Response(serializer_class.data, status=status.HTTP_200_OK)
            else:
                return error_response.serializer_error(self.__class__.__name__, request, serializer_class)

        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)

    def delete(self, request):
        """
        Delete an Employee by ID.
        """

        try:
            employee_id = request.query_params.get('employee_id')
            employee_data = getAllObjectWithFilter(Employee, {'employee_id': employee_id}).values('emp_user').first()
    
            if not employee_data:
                return Response(data=CommonApiMessages.does_not_exists('Employee'), status=status.HTTP_404_NOT_FOUND)

            user_id = employee_data['emp_user']
            Employee.objects.filter(employee_id=employee_id).delete()
            User.objects.filter(id=user_id).delete()

            return Response(data=CommonApiMessages.delete('Employee'), status=status.HTTP_200_OK)
        
        except RestrictedError:
            return Response(data=CommonApiMessages.restrict_delete('Employee'), status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)

# Employee DATATABLES ::
class EmployeeDataTableAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Summary or Description of the function:
            Get all Employee from Database with datatable format.
        """
        try:
            queryset = getAllObject(Employee).order_by('employee_id')
            data_table = json.loads(request.GET.get('data_table'))
            serializer_class = GetEmployeeDtSerializer

            searchField = ["employee_id","employee_image","username","employee_no","mobile_number","email","is_active"]
            columns = ["employee_id","employee_image","username","employee_no","mobile_number","email","is_active"]
            context = {'request': request}

            result = datatable.DataTablesServer(request=data_table, columns=columns, qs=queryset, context=context,
                                                searchField=searchField, serializer=serializer_class).output_result()
            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)

# Update Status For Employee
class UpdateStatusForEmployeeApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        """
        Update the active status for an employee by ID.
        """

        try:
            employee_id = request.query_params.get('employee_id')
            is_active = request.query_params.get('is_active')
            is_active = True if is_active == '1' else False
            with transaction.atomic():
                Employee.objects.filter(employee_id=employee_id).update(is_active=is_active)
                employee_data = getAllObjectWithFilter(Employee, {'employee_id': employee_id}).values('emp_user').first()
                
                if employee_data:
                    user_id = employee_data['emp_user']
                    User.objects.filter(id=user_id).update(is_active=is_active)
                else:
                    return Response(data=CommonApiMessages.does_not_exists('Employee'), status=status.HTTP_404_NOT_FOUND)
            return Response(data=CommonApiMessages.update_status('Employee'), status=status.HTTP_200_OK)

        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)
