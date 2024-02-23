from django.urls import path

from . import views

urlpatterns = [
    path("users/login", views.test_view, name="login"),
    path("users/info", views.users_info_view, name="users_info"),

    path("perf/createPlan", views.create_plan_view, name="create_plan"),
    path("perf/getPlanTableData", views.get_plan_view, name="get_plan"),
    path("run_task", views.run_task_view, name="run"),
]