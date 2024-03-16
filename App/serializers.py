from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Employee
        fields="__all__"
        # exclude=["groups","user_permissions",
        # "is_active"]
       
class PilotSerializer(serializers.ModelSerializer):
    class Meta:
        model=Pilot
        fields="__all__"
        # exclude=["groups","user_permissions",
        # "is_active"]

class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model=Bus
        exclude=["groups","user_permissions","is_active","date_joined","is_staff","is_superuser","last_login"]    
        # fields="__all__"

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Station
        fields=["station","id"] 
        # exclude=["groups","user_permissions","is_active","date_joined","is_staff","is_superuser","last_login"]    
                         
class UserSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()
    pilot = PilotSerializer()
    class Meta:
        model = User
        # fields="__all__"
        exclude=["groups","user_permissions","is_active","date_joined","is_staff","is_superuser","last_login"]    
