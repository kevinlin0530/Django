from rest_framework import serializers
from .models import Vendor 

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vendor
        # fields = '__all__'
        fields = [field.name for field in Vendor._meta.fields] 