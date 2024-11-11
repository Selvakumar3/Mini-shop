from django.shortcuts import render, redirect
from flourishapp.templatetags import permission_tags
from django.http import JsonResponse
import requests
from django.conf import settings
import json
from multiprocessing import context
from django import template
register = template.Library()
url = settings.API_URL

@register.simple_tag(takes_context=True)
def get_permission(context):

    request = context.get('request')
    user_id = request.session.get('user_id')
    token = request.session.get('token')

    if not user_id or not token:
        return redirect('login')
    headers = {
        'Authorization': f'Bearer {token}'
    }
    params = {'user_id': user_id}
    menu = requests.get('{url}/common/get-all-menus/'.format(url=url),params=params,headers=headers).json()
    return menu

@register.simple_tag(takes_context=True)
def get_user(context):
    request = context.get('request')
    user_id = request.session.get('user_id')
    token = request.session.get('token')

    if not user_id or not token:
        return redirect('login')
    headers = {
        'Authorization': f'Bearer {token}'
    }
    params = {"user_id":user_id}
    user=requests.get("{url}/user/get-profile/".format(url=url),headers=headers,params=params).json()
    return user

@register.simple_tag(takes_context=True)
def get_admin(context):
    request = context.get('request')
    user_id = request.session.get('user_id')
    token = request.session.get('token')

    if not user_id or not token:
        return redirect('login')
    headers = {
        'Authorization': f'Bearer {token}'
    }
    admin =  requests.get("{url}/settings/get-admin-settings/".format(url=url), headers=headers).json()
    return admin