from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# Create your models here.

class Station(models.Model):
    station = models.CharField(max_length=20,unique=True)
    def __str__(self):
        return self.station

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True,blank=True)
    # other attributes   
    def __str__(self):
        return self.user.username
    def clean(self):
        # Check if the username is already assigned to a Pilot
        if Pilot.objects.filter(user__username=self.user.username).exists():
            raise ValidationError('This username is already assigned to a Pilot.')
    
class Pilot(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True,blank=True)
    
    # other attributes   
    def __str__(self):
        return self.user.username
    def clean(self):
        # Check if the username is already assigned to an Employee
        if Employee.objects.filter(user__username=self.user.username).exists():
            raise ValidationError('This username is already assigned to an Employee.')

class Bus(models.Model):
    frm = models.ForeignKey(Station, related_name='departure_station', on_delete=models.SET_NULL,null=True,default="00NIL")
    to = models.ForeignKey(Station, related_name='destination_station', on_delete=models.SET_NULL,null=True,default="01NIL")
    regno = models.CharField(unique=True,max_length=20)
    lat = models.CharField(max_length=20,blank=True)
    long = models.CharField(max_length=20,blank=True)
    pilot = models.OneToOneField(Pilot,on_delete=models.CASCADE)
    def __str__(self):
        return self.regno