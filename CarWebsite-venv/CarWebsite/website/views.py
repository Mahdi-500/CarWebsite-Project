from django.shortcuts import render, redirect
from django.contrib import messages
from . import forms

from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from io import BytesIO

from .forms import CarForm
from .models import Cars
import requests
# Create your views here.

def MainView(request):
    return render(request, "main.html")

def AddCarView(request):
    if request.method == "POST":
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                Cars.objects.get(manufacturer=form.cleaned_data.get("manufacturer"),
                                car_model=form.cleaned_data.get("car_model"),
                                cylinders=form.cleaned_data.get("cylinders"),
                                engine_type=form.cleaned_data.get("engine_type"),
                                transmission=form.cleaned_data.get("transmission"),
                                fuel_type=form.cleaned_data.get("fuel_type"),
                                engine_volume=form.cleaned_data.get("engine_volume"),
                                drive_type=form.cleaned_data.get("drive_type"))
                
                messages.error(request, "this model is already registered")
            except Cars.DoesNotExist:
                messages.success(request, "car form submitted successfully")
                form.save()
            return redirect("website:main")
    else:
        form = CarForm()
    return render(request, "add_car.html", {"form":form})



def NHTSA_CarModelSearchFormView(request):
    result = []
    flag = False
    if request.method == "POST":
        form = forms.NHTSA_API_CarModelSearchForm(request.POST)
        if form.is_valid():
            flag = True
            temp = NHTSA_SearchResultsView(request, company_name=form.cleaned_data.get("query_company_name"),
                                        year=form.cleaned_data.get("query_year"),
                                        vehicle_type=form.cleaned_data.get("query_vehicle_type"))
            
            for i in temp:
                result.append(i["Model_Name"])
            result = sorted(result)
            context = {
                "form":form,
                "result":result,
                "flag":flag
            }

        else:
            context = {
                "form":form,
                "result":result,
                "flag":flag
            }
    else:
        form = forms.NHTSA_API_CarModelSearchForm()
        context = {
                "form":form,
                "result":result,
                "flag":flag
            }
    return render(request, "NHTSA/CarModel.html", context)
    


def NHTSA_SearchResultsView(request, company_name, year, vehicle_type):

    company_name = company_name.lower()
    url_values = {}
    url = 'https://vpic.nhtsa.dot.gov/api/vehicles/'
    if company_name:
        url_values["company_name"] = f'GetModelsForMake/{company_name}'
    
    if year:
        url_values["company_name"] = f"getmodelsformakeyear/make/{company_name}"
        url_values["year"] = f'/modelyear/{year}'

    if vehicle_type:
        url_values["company_name"] = f"getmodelsformakeyear/make/{company_name}"
        url_values["vehicle_type"] = f"/vehicleType/{vehicle_type}/"

    for i in url_values.keys():
        url += url_values[i]

    url += '?format=json'
    recieved = requests.get(url)
    r = BytesIO(recieved.content)
    parser = JSONParser()
    data = parser.parse(stream=r)
    items = data.get('Results', [])

    return items