import traceback
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import requests
url = settings.API_URL

# Admin Dashboard ::
def dashboard(request):
    return render(request,'dashboard.html')