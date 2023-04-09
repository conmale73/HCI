from django.urls import path
from . import views

urlpatterns = [
    path('', views.postnew, name='postnew'),
    path('postnew/<slug:postnew_slug>/', views.postnew_detail, name='postnew_detail'),
]