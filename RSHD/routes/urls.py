from django.urls import path

from . import views

urlpatterns = [
    path("", views.route, name="route"),
    path("<int:pk>/", views.popular_city, name="popular_city"),
]
