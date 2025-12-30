from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Formula1Data)
class Formula1DataAdmin(admin.ModelAdmin):
    list_display = ['winner_first_name', 'winner_last_name', 'grand_prix']
    search_fields = ['winner_first_name', 'winner_last_name', 'grand_prix', 'year']
    list_filter = ['grand_prix', 'team', 'year']
    list_per_page = 20

@admin.register(drivers)
class driversAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'number']
    search_fields = ['first_name', 'last_name', 'number']
    list_filter = ['number', 'nationality']
    list_per_page = 20

@admin.register(circuits)
class circuitAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'country']
    search_fields = ['name', 'country', 'ref_name', 'location']
    list_filter = ['country']
    list_per_page = 20

@admin.register(races)
class racesAdmin(admin.ModelAdmin):
    list_display = ['race_id','name', 'race_date']
    list_filter = ['year']
    search_fields = ['name', 'year']
    raw_id_fields = ['circuit_id']
    list_per_page = 20

@admin.register(constructors)
class constructorAdmin(admin.ModelAdmin):
    list_display = ['name', 'nationality']
    list_filter = ['nationality']
    search_fields = ['name', 'ref_name', 'nationality']
    list_per_page = 20

@admin.register(results)
class resultAdmin(admin.ModelAdmin):
    list_display = ['race_id', 'driver_id', 'constructor_id', 'car_number']
    list_filter = ['race_id', 'driver_id', 'constructor_id', 'starting_grid_position', 'final_position']
    search_fields = ['race_id__name', 'driver_id__first_name', 'driver_id__last_name', 'constructor_id__name']
    raw_id_fields = ['race_id', 'constructor_id', 'driver_id']
    list_per_page = 25