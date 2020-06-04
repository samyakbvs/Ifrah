from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('profile/<str:username>', views.Profile.as_view(),name='profile'),
    path('home',views.Home.as_view(),name='home'),
    path('add/<int:id>',views.AddToCart.as_view(),name='addToCart'),
    path('checkout',views.Checkout.as_view(),name='checkout'),
    path('remove/<int:id>',views.RemoveFromCart.as_view(),name='removeFromCart'),
    path('confirm/<str:uid>/',views.ConfirmOrder,name='confirmOrder'),
    path('logout',views.Logout.as_view(),name='logout'),
    path('details/<int:id>',views.ViewDetails.as_view(),name='viewDetails'),
    path('viewOrders',views.ViewOrders.as_view(),name='viewOrders'),
    path('team',views.Team.as_view(),name='team'),
    path('about',views.About.as_view(),name='about')
]
