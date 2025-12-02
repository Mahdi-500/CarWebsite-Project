from django.db import models
from django_resized import ResizedImageField

# Create your models here.
class Cars(models.Model):

    def saving_location(instance, filename):
        return f"{instance.manufacturer}/{instance.car_model}/{instance.engine_type}{instance.cylinders}/{filename}"
    class CylinderChoices(models.IntegerChoices):
        CY16 = 16, "16"
        CY12 = 12, "12"
        CY10 = 10, "10"
        CY8 = 8, "8"
        CY6 = 6, "6"
        CY5 = 5, "5"
        CY4 = 4, "4"
        CY3 = 3, "3"

    class EngineTypeChoices(models.TextChoices):
        V_type = "V", "V"
        W_type = "W", "W"
        I_type = "i", "inline(I)"
        B_type = "Boxer", "Boxer or Flat"
        WA_type = "Wankle", "Wankle"
        E_type = "Electric", "Electric"
        H_type = "Hybrid", "Hybrid"

    class TransmossionChoices(models.TextChoices):
        M = "Manual", "Manual"
        A = "Automatic", "Automatic"

    class FuelTypeChoices(models.TextChoices):
        G = "Gas", "Gasoline"
        D = "Diesel", "Diesel"
        H = "Hybrid", "Electricty - Gas"

    class DriveTypeChoices(models.TextChoices):
        RWD = "RWD", "Rear-Wheel-Drive"
        FWD = "FWD", "Front-Wheel-Drive"
        AWD = "AWD", "All-Wheel-Drive"
        WD4 = "4WD", "4-Wheel-Drive"

    class StatusChoices(models.TextChoices):
        ACCEPTED = "Accepted", "Accepted"
        DECLINED = "Declined", "Declined"
        DRAFT = "Draft", "Draft"

    class StatusManagrer(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status="Accepted")
        
    
    # ? overridng manager
    objects = models.Manager()  # default manager
    accepted = StatusManagrer() # new manager
    manufacturer = models.CharField(max_length=255, blank=False)
    car_model = models.CharField(max_length=255, blank=False, verbose_name="Model")
    cylinders = models.SmallIntegerField(choices=CylinderChoices.choices, blank=False)
    engine_type = models.CharField(max_length=10, choices=EngineTypeChoices.choices, blank=False, verbose_name="engine type")
    transmission = models.CharField(max_length=10, choices=TransmossionChoices.choices, blank=False,verbose_name="transmission type")
    fuel_type = models.CharField(max_length=10, choices=FuelTypeChoices.choices, blank=False, verbose_name="fuel type")
    engine_volume = models.DecimalField(max_digits=2, decimal_places=1, blank=False, verbose_name="engine volume (Liters)")
    drive_type = models.CharField(max_length=3, choices=DriveTypeChoices.choices, blank=False, verbose_name="drive type")
    image_1 = ResizedImageField(quality=100, upload_to=saving_location, verbose_name="image 1")
    image_2 = ResizedImageField(quality=100, upload_to=saving_location, verbose_name="image 2")
    image_3 = ResizedImageField(quality=100, upload_to=saving_location, verbose_name="image 3")
    details = models.TextField(blank=True, verbose_name="description")

    created = models.DateTimeField(auto_now_add=True)
    moified = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.DRAFT, verbose_name="status")



class GeneralInformation(models.Model):
    info = models.JSONField()