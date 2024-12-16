from django.db import models

##DIMENSION TABLES
class Driver(models.Model):
    driver_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=50)
    constructor = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Circuit(models.Model):
    circuit_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Climate(models.Model):
    climate_id = models.AutoField(primary_key=True)
    condition = models.CharField(max_length=50)
    temperature = models.FloatField()
    wind_speed = models.FloatField()

    def __str__(self):
        return self.condition

class Constructor(models.Model):
    constructor_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Race(models.Model):
    race_id = models.CharField(max_length=50, primary_key=True)
    season = models.IntegerField()
    round_number = models.IntegerField()
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.season} - Round {self.round_number}"
    
## FACT TABLES
class RaceResult(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    constructor = models.ForeignKey(Constructor, on_delete=models.CASCADE)
    position = models.IntegerField()
    points = models.FloatField()
    fastest_lap = models.FloatField(null=True, blank=True)
    time = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.race} - {self.driver.name}"

class RaceWeather(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    climate = models.ForeignKey(Climate, on_delete=models.CASCADE)
    date = models.DateField()
    temperature = models.FloatField()
    wind_speed = models.FloatField()

    def __str__(self):
        return f"{self.race} - {self.climate.condition}"