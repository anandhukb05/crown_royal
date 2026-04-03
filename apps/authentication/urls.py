from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),   # first page
    path('login/', views.login_view, name='login')
]