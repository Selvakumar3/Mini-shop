import traceback
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import requests
url = settings.API_URL

# Analytics Screen ::
def analytics_screen(request):
    return render(request,'mypanel/analytics/charts.html')

