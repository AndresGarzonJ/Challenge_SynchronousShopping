from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('api/v1/synchronous_shopping/', views.registerSynchronousShopping,
         name="registerSynchronousShopping")
]
