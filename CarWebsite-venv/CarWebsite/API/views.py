from rest_framework import viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from .serializer import *
from Formula1.models import *
# Create your views here.

class getF1Data(ListAPIView):
    serializer_class = formula1Serializer

    def get_queryset(self):
        data = {}
        for i,j in self.request.query_params.dict().items():
            data[i+"__icontains"] = j
        query_set = Formula1Data.objects.filter(**data)
        return query_set
    


class getDriverData(ListAPIView):
    serializer_class = f1DriverSerializer
    
    def get_queryset(self):
        data = {}
        parameters = self.request.query_params.dict().keys()
        if "name" in parameters or "nationality" in parameters or "number" in parameters:
            for i,j in self.request.query_params.dict().items():
                if i == "number":
                    data[i] = j
                else:
                    data[i+"__icontains"] = j
            query_set = drivers.objects.filter(**data)
        else:
            query_set = []
        return query_set



class getDriverResults(ListAPIView):
    serializer_class = f1ResultsSerializer

    def get_queryset(self):
        parameters = self.request.query_params.dict().keys()
        id = self.kwargs["id"]
        if parameters == []:
            query_set = results.objects.select_related("driver_id").filter(driver_id=id).order_by("final_position")
            
        
        elif "grid" in parameters:
            value = self.request.query_params.dict()["grid"]
            query_set = results.objects.select_related("driver_id").filter(driver_id=id, starting_grid_position=value).order_by("final_position")
        
        return query_set
    


class getCircuitData(ListAPIView):
    serializer_class = f1CircuitsSerializer

    def get_queryset(self):
        flag = False
        data = {}
        if self.request.path != "/api/F1/circuits/all":
            parameters = self.request.query_params.dict().keys()
            if "name" in parameters or "location" in parameters or "country" in parameters:
                
                if "name" in parameters and self.request.query_params.dict()["name"]:
                    query_set = circuits.objects.filter(ref_name__icontains=self.request.query_params.dict()["name"])
                    if query_set:
                        flag = True
                        return query_set
                if not flag:
                    for i,j in self.request.qury_params.dict().items():
                        data[i+"__icontains"] = j

                query_set = circuits.objects.filter(**data)
            else:
                query_set = []
        
        else:
            query_set = circuits.objects.all()

        return query_set
    


class getRaceData(ListAPIView):
    serializer_class = f1RacesSerializer

    def get_queryset(self):
        data = {}
        if self.request.path != "/api/F1/races/all":
            parameters = self.request.query_params.dict().keys()
            if "name" in parameters or "date" in parameters or "year" in parameters:
                for i,j in self.request.query_params.dict().items():
                    data[i+"__icontains"] = j
                query_set = races.objects.filter(**data)
            else:
                query_set = []
        
        else:
            query_set = races.objects.all()
        return query_set



class getConstructorData(ListAPIView):
    serializer_class = f1ConstructorsSerializer

    def get_queryset(self):
        if self.request.path != "/api/F1/constructors/all":
            if "nationality" in self.request.query_params.dict().keys():
                value = self.request.query_params.dict()["nationality"]
                query_set = constructors.objects.filter(nationality__icontains=value)
        else:
            query_set = constructors.objects.all()

        return query_set



class getSpecificResults(ListAPIView):
    serializer_class = f1ResultsSerializer

    def get_queryset(self):
        parameters = self.request.query_params.dict().keys()
        if "driver_id" in parameters and "year" in parameters:
            d_id = self.request.query_params.dict()['driver_id']
            year_data = self.request.query_params.dict()['year']
            query_set = results.objects.select_related("race_id").filter(driver_id=d_id, year=year_data)

        elif "name" in parameters and "year" in parameters:
            name = self.request.query_params.dict()['name']
            driver = drivers.objects.filter(ref_name__icontains=name)
            year_data = int(self.request.query_params.dict()['year'])
            data = results.objects.select_related("race_id").filter(driver_id=driver[0].driver_id).order_by("final_position")
            query_set = [i for i in data if i.race_id.year==year_data]
            
        return query_set