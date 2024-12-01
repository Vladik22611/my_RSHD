from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("your-name/", views.get_name, name="name"),
    path("test/", views.datef, name="test"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
]
