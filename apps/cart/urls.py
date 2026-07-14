from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('api/add/', views.cart_add, name='cart_add'),
    path('api/remove/', views.cart_remove, name='cart_remove'),
    path('api/update/', views.cart_update, name='cart_update'),
    path('api/summary/', views.cart_summary, name='cart_summary'),
    path('api/coupon/apply/', views.coupon_apply, name='coupon_apply'),
    path('api/coupon/remove/', views.coupon_remove, name='coupon_remove'),
]
