from django.urls import path, include

from . import views

urlpatterns = [
    path("add/race", views.add_route, name="add_route"),
    path("delete/race", views.del_route, name="del_route"),
    path("change/race", views.change_route, name="change_route"),
    path("change/race/<int:pk>/", views.change_route_def, name="change_route_def"),
    path("add/train/", views.add_train, name="add_train"),
    path("delete/train", views.del_train, name="del_train"),
    path("change/train", views.change_train, name="change_train"),
    path("change/train/<int:pk>", views.change_train_def, name="change_train_def"),
    path("add/model/", views.add_model, name="add_model"),
    path("delete/model", views.del_model, name="del_model"),
    path("change/model", views.change_model, name="change_model"),
    path("change/model/<int:pk>", views.change_model_def, name="change_model_def"),
    path("add/route/", views.add_it, name="add_it"),
    path("delete/route", views.del_it, name="del_it"),
    path("change/route", views.change_it, name="change_it"),
    path("change/route/<int:pk>", views.change_it_def, name="change_it_def"),
    path("add/station/", views.add_station, name="add_station"),
    path("delete/station/", views.del_station, name="del_station"),
    path("change/station/", views.change_station, name="change_station"),
    path(
        "change/station/<int:pk>", views.change_station_def, name="change_station_def"
    ),
]
