from django import forms
from .models import Cars

class CarForm(forms.ModelForm):
    class Meta:
        model = Cars
        fields = "__all__"
        exclude = ['created', 'modified', 'status']

    def clean(self):
        manufacturer = self.cleaned_data.get("manufacturer")
        car_model = self.cleaned_data.get("car_model")
        temp = car_model.split(" ")

        if not manufacturer.isalpha():
            raise forms.ValidationError("نام شرکت سازنده فقط باید حرف باشد")
        
        for i in temp:
            print(i)
            if not i.isalnum():
                raise forms.ValidationError("مدل ماشین نباید شامل کاراکتر های خاص باشد")
            
class NHTSA_API_CarModelSearchForm(forms.Form):

    VehicelTypeChoices = [
        ("", "----------------"),
        ("Passenger Car", "Passenger Car"),
        ("Truck", "Truck"),
        ("Multipurpose Passenger Vehicle (MPV)", "Multipurpose Passenger Vehicle (MPV)"),
        ("Low Speed Vehicle (LSV)", "Low Speed Vehicle (LSV)"),
        ("Off Road Vehicle", "Off Road Vehicle")
    ]        
    query_company_name = forms.CharField(label="company name*", max_length=255, widget=forms.TextInput(attrs={"placeholder": "Ford"}), required=True)
    query_year = forms.IntegerField(label="year", widget=forms.TextInput(attrs={"placeholder":"2015"}), required=False)
    query_vehicle_type = forms.ChoiceField(label="vehicle type", choices=VehicelTypeChoices, required=False)