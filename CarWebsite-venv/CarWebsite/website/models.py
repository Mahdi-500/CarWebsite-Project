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
        V_type = "V", "V (خورجینی)"
        W_type = "W", "W"
        I_type = "i", "inline(I) (خطی)"
        B_type = "Boxer", "Boxer or Flat"
        WA_type = "Wankle", "Wankle"
        E_type = "Electric", "Electric (برقی)"
        H_type = "Hybrid", "Hybrid (هیبرید)"

    class TransmossionChoices(models.TextChoices):
        M = "Manual", "Manual(دستی)"
        A = "Automatic", "Automatic (اتوماتیک)"

    class FuelTypeChoices(models.TextChoices):
        G = "Gas", "Gasoline (بنزین)"
        D = "Diesel", "Diesel (دیزل)"
        H = "Hybrid", "Electricty - Gas (برق - بنزین)"

    class DriveTypeChoices(models.TextChoices):
        RWD = "RWD", "Rear-Wheel-Drive (دیفرانسیل عقب)"
        FWD = "FWD", "Front-Wheel-Drive (دیفرانسیل جلو)"
        AWD = "AWD", "All-Wheel-Drive (4 چرخ محرک)"
        WD4 = "4WD", "4-Wheel-Drive (4 چرخ محرک)"

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
    manufacturer = models.CharField(max_length=255, blank=False, verbose_name="شرکت سازنده")
    car_model = models.CharField(max_length=255, blank=False, verbose_name="مدل")
    cylinders = models.SmallIntegerField(choices=CylinderChoices.choices, blank=False, verbose_name="تعداد سیلندر")
    engine_type = models.CharField(max_length=10, choices=EngineTypeChoices.choices, blank=False, verbose_name="نوع موتور")
    transmission = models.CharField(max_length=10, choices=TransmossionChoices.choices, blank=False,verbose_name="نوع گیربکس")
    fuel_type = models.CharField(max_length=10, choices=FuelTypeChoices.choices, blank=False, verbose_name="نوع سوخت")
    engine_volume = models.DecimalField(max_digits=2, decimal_places=1, blank=False, verbose_name="حجم موتور (لیتر)")
    drive_type = models.CharField(max_length=3, choices=DriveTypeChoices.choices, blank=False, verbose_name="نوع دیفرانسیل")
    image_1 = ResizedImageField(quality=100, upload_to=saving_location, verbose_name="عکس 1")
    image_2 = ResizedImageField(quality=100, upload_to=saving_location, verbose_name="عکس 2")
    image_3 = ResizedImageField(quality=100, upload_to=saving_location, verbose_name="عکس 3")
    details = models.TextField(blank=True, verbose_name="جزئیات")

    created = models.DateTimeField(auto_now_add=True)
    moified = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.DRAFT, verbose_name="وضعیت")