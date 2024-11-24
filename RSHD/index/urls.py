from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("your-name/", views.get_name, name="name"),
    path('test/',views.datef, name="test")
]
