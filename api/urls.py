from django.urls import path

from . import views

app_name = "api"
urlpatterns = [
    path("index", views.index, name="index"),
    path("run_by_id/<int:run_id>", views.runs_by_id, name="name_by_id"),
    path("new/<int:run_id>", views.create_run, name="create run"),
]
