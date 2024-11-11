from flourishapp.views import employee
from django.urls import path

urlpatterns = [
    path('', employee.employee_screen, name='employee'),
    path('employee-list/', employee.employee_list_screen, name='employee-list'),
    path('employee-dt/', employee.employee_dt, name='employee-dt'),
    path('edit-employee/', employee.edit_employee, name='edit-employee'),
    path('deleteemployee/', employee.delete_employee, name='deleteemployee'),
    path('update-employee-status/', employee.update_employee_status, name='update-employee-status'),
]