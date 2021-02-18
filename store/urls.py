from django.urls import path
from . import views


urlpatterns = [
    path('',views.store,name="home"),
    path('login/',views.user_login,name="login"),
    path('cart/',views.cart,name="cart"),
    path('logout/',views.user_logout,name="logout"),
    path('signup/',views.user_signup,name="signup"),
    path('checkout/',views.checkout,name="checkout"),
    path('orders/',views.orders,name="orders"),
]

