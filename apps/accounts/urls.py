from django.urls import path

from . import views


app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('registro/', views.register_view, name='register'),
    path('salir/', views.logout_view, name='logout'),
    path('api/registro/', views.register_api, name='register_api'),
    path('api/newsletter/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('api/favoritos/toggle/', views.wishlist_toggle, name='wishlist_toggle'),
    path('perfil/', views.profile_view, name='profile'),
    path('favoritos/', views.wishlist_view, name='wishlist'),
]
