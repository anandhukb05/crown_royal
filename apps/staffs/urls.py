# polls/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.hello_world_view1, name="hello_world_view1"),

]
