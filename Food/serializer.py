from rest_framework import serializers
from .models import Food
import django_filters


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model=Food
        # fields = '__all__'
        fields = [field.name for field in Food._meta.fields] 


class FoodFilter(django_filters.FilterSet):

    class Meta:
        model = Food
        fields = '__all__'