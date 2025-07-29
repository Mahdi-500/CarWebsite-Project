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