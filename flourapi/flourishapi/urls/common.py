from django.urls import path
from flourishapi.views.common import *

urlpatterns = [
    path('log/', LogAPI.as_view()),
    path('log-dt/', LogReportAPI.as_view()),

    # Usergroup urls::
    path('getallusergroupapi/', UserGroupMenuApi.as_view()),
    path('getusergroupmenu/',UserGroupMenuListApi.as_view(),name='getusergroupmenu'),
    path('postusergroupmenu/',UserGroupMenuListApi.as_view(),name='postusergroupmenu'),
    path('updateusergroupmenu/',UpdateUserGroupMenuAPI.as_view(),name='updateusergroupmenu'),
    path('deleteusergroupmenu/',UpdateUserGroupMenuAPI.as_view(),name='deleteusergroupmenu'),
    path('getusergrouplist/',GetUserGroupListAPI.as_view(),name='getusergrouplist'),
    path('usergroupmenudatatable/',GetUserdatatableAPI.as_view(),name='usergroupmenudatatable'),

    path('generatecode/',GetGenerateCodeApi.as_view(),name='generatecode'),
    path('get-bill-type/',GetBillTypeAPI.as_view(),name='get-bill-type'),
    path('get-all-menus/',getallmenuApi.as_view(),name='get-all-menus'),

    # Dashboard
    path('get-weekly-amt/',WeeklyNetAmountView.as_view(),name='get-weekly-amt'),

    ]