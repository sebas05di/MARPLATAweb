from django.urls import path

from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('buscar/', views.search, name='search'),
    path('api/sugerencias/', views.search_suggestions, name='search_suggestions'),
    path('<slug:collection_slug>/', views.product_list, name='product_list_by_collection'),
]
