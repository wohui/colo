from django.urls import path

from . import views


urlpatterns = [


    path("createTestMachine", views.create_test_machine_view, name="create"),
    path("updateTestMachine", views.update_test_machine_view, name="update"),
    path("deleteTestMachine", views.delete_test_machine_view, name="delete"),
    path("applyTestMachine", views.apply_test_machine_view, name="apply"),
    path("getTestMachineData", views.get_test_machine_view, name="get"),

]