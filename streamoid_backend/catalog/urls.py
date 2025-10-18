from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_csv),
    path('products/', views.list_products),
    path('products/search/', views.search_products),
]
