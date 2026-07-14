from django.urls import path

from . import views


app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout_form, name='checkout_form'),
    path('checkout/whatsapp/', views.checkout_whatsapp, name='checkout_whatsapp'),
    path('orden/<str:order_number>/exito/', views.order_success, name='order_success'),
    path('orden/<str:order_number>/', views.order_tracking, name='order_tracking'),
    path('rastrear/', views.tracking_lookup, name='tracking_lookup'),
]
