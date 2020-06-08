from django.shortcuts import render,redirect,get_object_or_404
from rest_framework.views import APIView
from .models import UserProfile,Painting,Cart,Order,Member
from django.contrib.auth.models import User
from django.contrib import auth
from .PayTm import Checksum
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import uuid

MERCHANT_KEY = 'RFXkcY7NUTsKgces'

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
        paintings = Painting.objects.exclude(c_paintings = user.cart)
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
    def post(self,request):
        # amount = request.POST['Amount']
        # uid = str(uuid.uuid1())
        # donation = Donation(amount=amount,user=request.user,uid=uid)
        # donation.save()
        user = request.user
        uid = str(uuid.uuid1())
        paintings = user.cart.paintings.all()
        order = Order.objects.create(user=user)
        order.uid = uid
        bill = 0
        for painting in paintings:
            order.paintings.add(painting)
            bill += painting.price
        order.bill =  bill + 10
        order.save()

        param_dict = {
            'MID':'DhKcem03471021583928',
            'ORDER_ID': order.uid,
            'TXN_AMOUNT': str(order.bill),
            'CUST_ID': str(request.user.userprofile.email),
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'WEBSTAGING',
            'CHANNEL_ID':'WEB',
            'CALLBACK_URL':'https://ifrah.in/gallery/confirm/'+str(order.uid)+'/',
	        # 'CALLBACK_URL':'http://127.0.0.1:8000/gallery/confirm/'+str(order.uid)+'/',
        }

        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict,MERCHANT_KEY)
        return render(request, 'Gallery/paytm.html', {'param_dict':param_dict})


@csrf_exempt
def ConfirmOrder(request,uid):

    form = request.POST
    response_dict={}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            Temp_checksum = response_dict[i]
    verify = Checksum.verify_checksum(response_dict,MERCHANT_KEY,Temp_checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            order =  get_object_or_404(Order,uid=uid)
            user = order.user
            order.successful = True
            order.save()
            for painting in user.cart.paintings.all():
                painting.sold = True
                painting.save()
            order.user.cart.paintings.clear()
            return render(request,'Gallery/ThankYou.html')
        else:
            order =  get_object_or_404(Donation,uid=uid)
            order.delete()
            return render(request,'Gallery/ThankYou.html',{'error':'An error occured, please try again later!'})
    else:
        return render(request,'Gallery/ThankYou.html',{'error':'An error occured, please try again later!'})

# class ConfirmOrder(APIView):
#     @method_decorator(login_required)
#     @csrf_exempt
#     def post(self,request,uid):
#         form = request.POST
#         response_dict={}
#         for i in form.keys():
#             response_dict[i] = form[i]
#             if i == 'CHECKSUMHASH':
#                 Temp_checksum = response_dict[i]
#         verify = Checksum.verify_checksum(response_dict,MERCHANT_KEY,Temp_checksum)
#         if verify:
#             if response_dict['RESPCODE'] == '01':
#                 order =  get_object_or_404(Order,uid=uid)
#                 order.succesful = True
#                 order.save()
#                 for painting in user.cart.paintings.all():
#                     painting.sold = True
#                     painting.save()
#                 order.user.cart.paintings.clear()
#                 return render(request,'Gallery/ThankYou.html')
#             else:
#                 order =  get_object_or_404(Donation,uid=uid)
#                 order.delete()
#                 return render(request,'Gallery/ThankYou.html',{'error':'An error occured, please try again later!'})
#         else:
#             return render(request,'Gallery/ThankYou.html',{'error':'An error occured, please try again later!'})

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

# class Donate(APIView):
#
#         param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict,MERCHANT_KEY)
#         return render(request, 'Account/paytm.html', {'param_dict':param_dict})
#     def get(self,request):
#         return render(request,'Account/Donate.html')
