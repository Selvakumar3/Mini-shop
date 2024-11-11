from django.urls import path
from flourishapi.views.masters import *

urlpatterns = [
    # Category URLS
    path("category-dt-api/", CategoryDataTableAPI.as_view()),
    path("get-all-category/", CreateCategoryAPI.as_view()),
    path("post-category/", CreateCategoryAPI.as_view()),
    path("edit-category/", CategoryUpdateAPI.as_view()),
    path("put-category/", CategoryUpdateAPI.as_view()),
    path("delete-category/", CategoryUpdateAPI.as_view()),
    path("update-category-status/", updateStausForCategoryApi.as_view()),
    
    # Brand URLS
    path("brand-dt-api/", BrandDataTableAPI.as_view()),
    path("get-all-brand/", CreateBrandAPI.as_view()),
    path("post-brand/", CreateBrandAPI.as_view()),
    path("edit-brand/", BrandUpdateAPI.as_view()),
    path("put-brand/", BrandUpdateAPI.as_view()),
    path("delete-brand/", BrandUpdateAPI.as_view()),
    path("update-brand-status/", updateStausForbrandApi.as_view()),

    # Unit URLS
    path("unit-dt-api/",UnitDataTableAPI.as_view()),
    path("get-all-unit/", CreateUnitAPI.as_view()),
    path("post-unit/", CreateUnitAPI.as_view()),
    path("edit-unit/", UnitUpdateAPI.as_view()),
    path("put-unit/", UnitUpdateAPI.as_view()),
    path("delete-unit/", UnitUpdateAPI.as_view()),
 
    # Product URLS
    path("product-dt-api/",ProductDataTableAPI.as_view()),
    path("get-all-product/", CreateProductAPI.as_view()),
    path("post-product/", CreateProductAPI.as_view()),
    path("edit-product/", ProductUpdateAPI.as_view()),
    path("put-product/", ProductUpdateAPI.as_view()),
    path("delete-product/", ProductUpdateAPI.as_view()),
    path("update-product-status/", updateStausForProductApi.as_view()),

    # Employee URLS
    path("employee-dt-api/",EmployeeDataTableAPI.as_view()),
    path("get-all-employee/", CreateEmployeeAPI.as_view()),
    path("post-employee/", CreateEmployeeAPI.as_view()),
    path("edit-employee/", EmployeeUpdateAPI.as_view()),
    path("put-employee/", EmployeeUpdateAPI.as_view()),
    path("delete-employee/", EmployeeUpdateAPI.as_view()),
    path("update-employee-status/", UpdateStatusForEmployeeApi.as_view()),

]