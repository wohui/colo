from django.urls import path

from . import views

urlpatterns = [
    path("test", views.test_view, name="index"),
    path("create_task", views.create_task_view, name="create"),
    path("run_task", views.run_task_view, name="run"),
]