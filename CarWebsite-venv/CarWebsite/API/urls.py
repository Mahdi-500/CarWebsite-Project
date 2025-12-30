from django.urls import path, re_path
from . import views

app_name = "API"
urlpatterns = [
    path("F1", views.getF1Data.as_view(), name="main"),
    path("F1/drivers", views.getDriverData.as_view(), name="all_driver"),
    path("F1/driver/<int:id>/results", views.getDriverResults.as_view(), name="driver_results"),
    path("F1/circuits", views.getCircuitData.as_view(), name="circuits"),
    path("F1/circuits/all", views.getCircuitData.as_view(), name="all_circuit_data"),
    path("F1/races", views.getRaceData.as_view(), name="races"),
    path("F1/races/all", views.getRaceData.as_view(), name="all_races_data"),
    path("F1/constructors", views.getConstructorData.as_view(), name="constructor"),
    path("F1/constructors/all", views.getConstructorData.as_view(), name="all_constructors"),
    path("F1/results", views.getSpecificResults.as_view(), name="specific_result"),
]
