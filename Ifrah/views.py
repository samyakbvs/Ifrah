from django.shortcuts import render,redirect
from rest_framework.views import APIView
from django.core.validators import validate_email
from django.contrib import auth
from django.contrib.auth.models import User

# Create your views here.
class Login(APIView):
    def get(self,request):
        return render(request,'Gallery/login.html')
    def post(self,request):
        user = auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            try:
                user_name = user.userprofile.name
                auth.login(request,user)
                return redirect('home')
            except:
                return redirect('profile',user.username)
        else:
            return render(request,'Gallery/login.html',{'error':'User does not exist'})

class Signup(APIView):
    def get(self,request):
        return render(request,'Gallery/signup.html')
    def post(self,request):
        if request.POST['password'] == request.POST['verifypassword']:
            try:
                print(request.POST['username'])
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'Gallery/signup.html', {'error':'Account already exists'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password= request.POST['password'])
                # user = User(request.POST['username'], password= request.POST['password'])
                return redirect('profile',user.username)
        else:
            return render(request,'Gallery/signup.html',{'error':'Passwords do not match'})

class Logout(APIView):
    def get(self,request):
        auth.logout(request)
        return redirect('login')
