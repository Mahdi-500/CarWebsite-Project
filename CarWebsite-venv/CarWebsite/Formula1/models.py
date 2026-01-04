from django.db import models

# Create your models here.
class Formula1Data(models.Model):
    date = models.DateField()
    continent = models.CharField(max_length=15)
    grand_prix = models.CharField(max_length=15)
    circuit = models.CharField(max_length=50)
    winner_first_name = models.CharField(max_length=40)
    winner_last_name = models.CharField(max_length=100)
    team = models.CharField(max_length=30)
    time = models.DurationField()
    laps = models.SmallIntegerField()
    year = models.IntegerField()



class drivers(models.Model):
    driver_id = models.BigAutoField(primary_key=True)
    ref_name = models.CharField(max_length=100)
    number = models.PositiveSmallIntegerField(default=0)
    code  = models.CharField(max_length=3)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=60)

    def __str__(self):
        return self.first_name + " " + self.last_name
    
    class Meta:
        verbose_name = 'driver'
        verbose_name_plural = 'drivers'

class circuits(models.Model):
    circuit_id = models.BigAutoField(primary_key=True)
    ref_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.FloatField(blank=True, null=True, default=None)
    longitude = models.FloatField(blank=True, null=True, default=None)
    altitude = models.FloatField(blank=True, null=True, default=None)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'circuit'
        verbose_name_plural = 'circuits'

class races(models.Model):
    race_id = models.BigAutoField(primary_key=True)
    circuit_id = models.ForeignKey(circuits, on_delete=models.PROTECT, related_name="races")
    year = models.IntegerField()
    round = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    fp1_date = models.DateField(blank=True, null=True, default=None)
    fp1_time = models.TimeField(blank=True, null=True, default=None)
    fp2_date = models.DateField(blank=True, null=True, default=None)
    fp2_time = models.TimeField(blank=True, null=True, default=None)
    fp3_date = models.DateField(blank=True, null=True, default=None)
    fp3_time = models.TimeField(blank=True, null=True, default=None)
    sprint_quali_date = models.DateField(blank=True, null=True, default=None)
    sprint_quali_time = models.TimeField(blank=True, null=True, default=None)
    sprint_race_date = models.DateField(blank=True, null=True, default=None)
    sprint_race_time = models.TimeField(blank=True, null=True, default=None)
    quali_date = models.DateField(blank=True, null=True, default=None)
    quali_time = models.TimeField(blank=True, null=True, default=None)
    race_date = models.DateField(blank=True, null=True, default=None)
    race_time = models.TimeField(blank=True, null=True, default=None)

    def __str__(self):
        return f"{self.name} in {self.year}"
    
    class Meta:
        verbose_name = 'race'
        verbose_name_plural = 'races'



# todo - shows the drivers standings in one season
class driverStandings(models.Model):
    ds_id = models.BigAutoField(primary_key=True)
    race_id = models.ForeignKey(races, on_delete=models.PROTECT, related_name="season_driver_standing")
    driver_id = models.ForeignKey(drivers, on_delete=models.PROTECT, related_name="season_driver_standing")
    points = models.SmallIntegerField()
    position = models.SmallIntegerField()
    wins_in_season = models.SmallIntegerField()

    class Meta:
        verbose_name = 'driver standing'
        verbose_name_plural = 'driver standings'



class constructors(models.Model):
    constructor_id = models.BigAutoField(primary_key=True)
    ref_name = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'constructor'
        verbose_name_plural = 'constructors'

class results(models.Model):
    result_id = models.BigAutoField(primary_key=True)
    race_id = models.ForeignKey(races, on_delete=models.PROTECT, related_name="results")
    driver_id = models.ForeignKey(drivers, on_delete=models.PROTECT, related_name="results")
    constructor_id = models.ForeignKey(constructors, on_delete=models.PROTECT, related_name="results")
    car_number = models.SmallIntegerField()
    starting_grid_position = models.SmallIntegerField()
    final_position = models.CharField(max_length=5)
    points = models.SmallIntegerField()
    laps = models.SmallIntegerField()
    time = models.CharField(max_length=20, null=True, default=None)
    fastest_lap = models.DurationField()
    top_speed_of_fl = models.FloatField(verbose_name="fastest lap top speed") # ? fl = fastest lap

    def __str__(self):
        return f"results of {self.driver_id.first_name} {self.driver_id.last_name} for {self.race_id}"
    
    class Meta:
        verbose_name = 'Result'
        verbose_name_plural = 'Results'