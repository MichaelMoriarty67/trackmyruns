from django.urls import path

from . import views

app_name = "api"
urlpatterns = [
    path("runs/<int:run_id>", views.run_by_id, name="name_by_id"),
    path("runs", views.runs, name="runs"),
    path("user", views.user, name="user"),
    path("user/<int:user_id>", views.user_by_id, name="user_by_id"),
]
