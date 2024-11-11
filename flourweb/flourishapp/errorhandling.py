from django.shortcuts import render
from django.http import HttpResponse

def custom_404_view(request,exception):
    return render(request, '404.html',status=404)

# def custom_500_view(request):
#     return render(request, '500.html', status=500)