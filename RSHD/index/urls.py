from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("route/", views.route, name="route"),
    path("your-name/", views.get_name, name="name"),
]
