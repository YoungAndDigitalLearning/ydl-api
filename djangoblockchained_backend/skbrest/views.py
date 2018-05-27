from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import login, authenticate

# Create your views here.

def authenticate_user(request):
    if request.method == "POST":
        
        user = request.POST.get("username")
        passw = request.POST.get("password")
        isValidUser = authenticate(username = user, password = passw)

        if isValidUser:

            return JsonResponse({"result": True})
        else:

            return JsonResponse({"result": False})