from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Cars)
class CarsAdmin(admin.ModelAdmin):
    list_display = ["manufacturer", "car_model"]