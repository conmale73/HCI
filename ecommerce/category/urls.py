from django.urls import path
from . import views

urlpatterns = [
    path('', views.btn_category, name='category')
]