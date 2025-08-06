from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "website"
urlpatterns = [
    path("", views.MainView, name="main"),
    path("add_car/", views.AddCarView, name="add_car"),
    path("search_model/", views.NHTSA_CarModelSearchFormView, name="NHTSA_MY_search"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)