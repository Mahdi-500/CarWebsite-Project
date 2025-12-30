from django.urls import path
from .views import *

app_name = "Formula1"
urlpatterns = [
    path("", main_view, name="main"),
    path("circuits", circuit_list_view, name="circuit_list"),
    path("circuits/<int:id>/details", circuit_detail_view, name="circuit_details"),
    path("circuits/<int:c_id>/details/race_results/<int:r_id>/details", race_details_view, name="circuit_race_detail"),
    path("races", race_list_view, name="races_list"),
    path("races/<int:r_id>/details", race_details_view, name="race_details"),
    path("drivers", driver_list_view, name="drivers_list"),
    path("drivers/<int:id>/details", driver_details_view, name="driver_details"),
    path("teams", teams_list_view, name="teams_list")
]
