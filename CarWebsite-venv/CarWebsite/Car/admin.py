from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(submittingNewCars)
class submittingNewCarsAdmin(admin.ModelAdmin):
    list_display = ["manufacturer", "car_model"]

@admin.register(GeneralInformation)
class GeneralInformationAdmin(admin.ModelAdmin):
    list_display = ["info"]