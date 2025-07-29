from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CarForm
from .models import Cars
import requests
# Create your views here.

def MainView(request):
    url = 'https://www.carapi.app/api/engines/v2?cylinders=8'
    r = requests.get(url)
    print(r.text)	
    raise ValueError
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
                
                messages.error(request, "این مدل از ماشین قبلا ثبت شده است")
            except Cars.DoesNotExist:
                messages.success(request, ("فرم شما با موفقیت ثبت شد"))
                form.save()
            return redirect("website:main")
    else:
        form = CarForm()
    return render(request, "add_car.html", {"form":form})
