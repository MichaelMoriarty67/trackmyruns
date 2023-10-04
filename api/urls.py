from django.urls import path

from . import views

app_name = "api"
urlpatterns = [
    path("runs", views.runs, name="runs"),
    path("runs/<int:run_id>", views.run_by_id, name="run_by_id"),
    path("runs/<int:run_id>/map", views.run_map_by_id, name="run_map_by_id"),
    path("register", views.register, name="register"),
    path("user", views.user, name="user"),
]
