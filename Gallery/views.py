from django.shortcuts import render,redirect
from rest_framework.views import APIView
from .models import UserProfile,Painting,Cart,Order,Member
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
class Profile(APIView):
    def get(self,request,username):
        return render(request,'Gallery/profile.html',{'username':username})
    def post(self,request,username):
        name = request.POST['name']
        address = request.POST['address']
        pincode = request.POST['pincode']
        city = request.POST['city']
        # age = request.POST['age']
        email = request.POST['email']
        user = User.objects.get(username=username)

        profile = UserProfile(name=name,address=address,pincode=pincode,city=city,email=email,user=user)
        profile.save()

        cart = Cart(user=user)
        cart.save()

        auth.login(request,user)

        return redirect('home')


class Home(APIView):
    @method_decorator(login_required)
    def get(self,request):
        user = request.user
        # paintings = user.cart.paintings.all()
        paintings = Painting.objects.exclude(c_paintings = user.cart).exclude(sold=True)
        print(len(paintings))
        return render(request,'Gallery/home.html',{'paintings':paintings})

class AddToCart(APIView):
    @method_decorator(login_required)
    def get(self,request,id):
        painting = Painting.objects.get(id=id)
        request.user.cart.paintings.add(painting)
        return redirect('home')

class RemoveFromCart(APIView):
    @method_decorator(login_required)
    def get(self,request,id):
        painting = Painting.objects.get(id=id)
        request.user.cart.paintings.remove(painting)
        return redirect('checkout')


class Checkout(APIView):
    @method_decorator(login_required)
    def get(self,request):
        user = request.user
        paintings = user.cart.paintings.all()
        bill = 0
        for painting in paintings:
            bill += painting.price
        return render(request,'Gallery/checkout.html',{'paintings':paintings,'bill':bill})

class ConfirmOrder(APIView):
    @method_decorator(login_required)
    def get(self,request):
        user = request.user
        paintings = user.cart.paintings.all()
        order = Order.objects.create(user=user)
        bill = 0
        for painting in paintings:
            bill += painting.price
            order.paintings.add(painting)
        order.bill = bill
        order.save()
        for painting in user.cart.paintings.all():
            painting.sold = True
            painting.save()
        user.cart.paintings.clear()
        return redirect('checkout')

class Logout(APIView):
    @method_decorator(login_required)
    def get(self,request):
        auth.logout(request)
        return redirect('login')

class ViewDetails(APIView):
    @method_decorator(login_required)
    def get(self,request,id):
        painting = Painting.objects.get(id=id)
        return render(request,'Gallery/details.html',{'painting':painting})

class ViewOrders(APIView):
    @method_decorator(login_required)
    def get(self,request):
        user = request.user
        orders = user.orders.all()
        return render(request,'Gallery/viewOrders.html',{'orders':orders})

class Team(APIView):
    @method_decorator(login_required)
    def get(self,request):
        Team = Member.objects.all()
        return render(request,'Gallery/team.html',{'Team':Team})

class About(APIView):
    def get(self,request):
        return render(request,'Gallery/about.html')
