from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# Disable CRSF token
@csrf_exempt
def authenticate_user(request):
    if request.method == "POST":
        
        user = request.POST.get("username")
        passw = request.POST.get("password")
        isValidUser = authenticate(username = user, password = passw)

        if isValidUser:

            return JsonResponse({"result": True})
        else:

            return JsonResponse({"result": False})

#@api_view(["POST"])
#def register_user(request):
#    pass