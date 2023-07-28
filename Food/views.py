from django.shortcuts import render
from .models import Food
from vendor.models import Vendor
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView , CreateView
from django.utils.translation import gettext_lazy as _
from rest_framework import generics
from .serializer import FoodSerializer ,FoodFilter
from rest_framework.permissions import AllowAny
from django.db.models.fields.files import ImageFieldFile
from decimal import Decimal
from rest_framework import viewsets , status
from datetime import date, datetime
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser , IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication ,TokenAuthentication
from rest_framework.parsers import JSONParser ,FormParser,MultiPartParser
# Create your views here.


class FoodModel(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    def create(self, request):

        try:
            food_name = request.POST.get('food_name')
            vendor_name = request.POST.get('food_vendor')
            queryset = Vendor.objects.filter(vendor_name=vendor_name)
            if bool(queryset) != True:
                result = {'status':"攤販名稱不存在"}
                return Response(result,status=status.HTTP_404_NOT_FOUND)
            
            serializer = FoodSerializer(data = request.POST)
            if serializer.is_valid():
                queryset = Food.objects.filter(food_name = food_name,food_vendor = vendor_name)
                if not queryset.exists():
                    serializer.save()
                    return Response(serializer.data , status=status.HTTP_201_CREATED)
                else:
                    result = {'status':'商品已存在'}
                    return Response(result , status=status.HTTP_400_BAD_REQUEST)
                
        except Food.DoesNotExist:
            result = {'status':'未知錯誤'}
            return Response(result,status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request):

        food_names = request.POST.get('food_name').split(',')
        queryset_all = Food.objects.all().filter(food_name__in=food_names)

        if len(food_names) >= 1 and queryset_all.exists():
            serializer = FoodSerializer(queryset_all,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        result = {"status":"查無資料"}
        return Response(result , status=status.HTTP_404_NOT_FOUND)

    def update(self,request,*args,**kwargs):

        food_name = kwargs.get('pk')
        food_vendor = request.data.get('food_vendor')
        
        try:
            queryset = Food.objects.get(food_name = food_name, food_vendor=food_vendor)
            
        except Food.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = FoodSerializer(queryset,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def Clients(request):
    if request.method == 'POST':
        try:
            food_name = request.POST.get('food_name')
            vendor_name = request.POST.get('food_vendor')
            queryset = Vendor.objects.filter(vendor_name=vendor_name)
            if bool(queryset) != True:
                result = {"status":"攤販名稱不存在"}
                return Response(result,status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            result = {"status":"未知錯誤"}
            return Response(result,status=status.HTTP_400_BAD_REQUEST)


        try:
            serializer = FoodSerializer(data = request.POST)
            if serializer.is_valid():
                queryset = Food.objects.filter(food_name = food_name,food_vendor=vendor_name)
                if not queryset.exists():
                    serializer.save()
                    return Response(serializer.data , status=status.HTTP_201_CREATED)
                else:
                    result = {"status":"商品已存在"}
                    return Response(result,status=status.HTTP_400_BAD_REQUEST)
        except Food.DoesNotExist:
            result = {"status":"未知錯誤"}
            return Response(result,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def Clients_Check(request):
    
    if request.method == 'GET':
        try:
            food_name = request.data.get('food_name').split(',')
            queryset = Food.objects.all().filter(food_name__in=food_name)
            if queryset.exists() and len(food_name)>=1:
                serializer = FoodSerializer(queryset,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            result = {"status":"查無資料"}
            return Response(result , status=status.HTTP_404_NOT_FOUND)
        except Food.DoesNotExist:
            result = {"status":"查無資料"}
            return Response(result , status=status.HTTP_404_NOT_FOUND)
        
