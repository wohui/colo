from django.urls import path

from . import views

urlpatterns = [
    path("users/login", views.test_view, name="login"),
    path("users/info", views.users_info_view, name="users_info"),

    path("perf/createPlan", views.create_plan_view, name="create_plan"),
    path("perf/updatePlan", views.update_plan_view, name="update_plan"),
    path("perf/getPlanTableData", views.get_plan_view, name="get_plan"),
    path("perf/executePlan", views.execute_plan_view, name="exec_plan"),

    path("perf/getTestRecord", views.get_test_record_view, name="test_record"),
    path("perf/stopExecutePlan", views.stop_execute_plan_view, name="stop_test"),

    path("perf/getAllScript", views.get_all_script_view, name="get_all_script"),

    path("run_task", views.run_task_view, name="run"),
]