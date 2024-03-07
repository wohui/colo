from django.urls import path

from . import views
from .sys_config import views as sys_config_views

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

    path("test/start", views.start_locust_view, name="start"),
    path("test/stop", views.stop_locust_view, name="stop"),

    # sysconfig
    path("sysConfig/createConfig", sys_config_views.create_config_view, name="create_config"),
    path("sysConfig/deleteConfig", sys_config_views.delete_config_view, name="delete_config"),
    path("sysConfig/updateConfig", sys_config_views.update_config_view, name="update_config"),
    path("sysConfig/getConfig", sys_config_views.get_config_view, name="get_config"),
]
