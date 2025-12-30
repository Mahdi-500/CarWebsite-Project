from rest_framework.serializers import ModelSerializer
from Formula1.models import *

class formula1Serializer(ModelSerializer):
    class Meta:
        model = Formula1Data
        fields = "__all__"

class f1DriverSerializer(ModelSerializer):
    class Meta:
        model = drivers
        fields = "__all__"

class f1CircuitsSerializer(ModelSerializer):
    class Meta:
        model = circuits
        fields = "__all__"

class f1RacesSerializer(ModelSerializer):
    class Meta:
        model = races
        fields = "__all__"

class f1ResultsSerializer(ModelSerializer):
    class Meta:
        model = results
        fields = "__all__"

class f1ConstructorsSerializer(ModelSerializer):
    class Meta:
        model = constructors
        fields = "__all__"