from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "website"
urlpatterns = [
    path("add_car/", views.AddCarView, name="add_car"),
    path("", views.MainView, name="main")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)