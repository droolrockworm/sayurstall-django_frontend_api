from django.urls import path

from . import views

urlpatterns = [
    path('get_products/', views.get_products),
    

]
