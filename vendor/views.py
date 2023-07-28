from django.shortcuts import render
from .models import Vendor
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView , CreateView
from django.utils.translation import gettext_lazy as _
from rest_framework import generics
from .serializer import MyModelSerializer
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
from rest_framework.decorators import api_view
from django.db.models import Q
# Create your views here.

class VendorListView(ListView):  # 繼承listView (CBV)
    model = Vendor

class VendorList(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    def create(self,request):
        serializer = MyModelSerializer(data = request.data)
        if serializer.is_valid():
            vendor_name = request.data.get('vendor_name')
            queryset = Vendor.objects.filter(vendor_name=vendor_name)
            if not queryset.exists():
                serializer.save()
                return Response(serializer.data , status=status.HTTP_201_CREATED)
        result = {"error":"名稱已存在"}
        return Response(result,status=status.HTTP_400_BAD_REQUEST)
    
    def list(self,request):
        vendor_names = request.POST.get('vendor_name')
        address = request.POST.get('address')
        store_name = request.POST.get('store_name')
        if vendor_names:
            vendor_names = request.POST.get('vendor_name').split(',')
            query = Q()
            for name in vendor_names:
                query |=Q(vendor_name__icontains=name)
            # queryset = Vendor.objects.filter(vendor_name__in=vendor_names)
            queryset = Vendor.objects.filter(query)
            if queryset.exists():
                serializer = MyModelSerializer(queryset,many=True )
                return Response(serializer.data,status=status.HTTP_200_OK)
            result = {"error":"查無此筆資料"}
            return Response(result,status=status.HTTP_404_NOT_FOUND)
        elif address:
            address = request.data.get('address').split(',')
            #! 模糊搜索
            query = Q()
            # queryset = Vendor.objects.filter(address__in=addres)
            for a in address:
                query |=Q(address__icontains=a)
            queryset = Vendor.objects.filter(query)
            if queryset.exists():
                serializer = MyModelSerializer(queryset,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
        elif store_name:
            store_names = request.POST.get('store_name').split(',')
            query = Q()
            for name in store_names:
                query |=Q(store_name__icontains = name)
            queryset = Vendor.objects.filter(query)
            if queryset.exists():
                serializer = MyModelSerializer(queryset,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            
            result = {"error":"查無此筆資料"}
            return Response(result,status=status.HTTP_404_NOT_FOUND)

    def update(self, request,*args, **kwargs):
        vendor_name = kwargs.get('pk')
        try:
            queryset = Vendor.objects.get(vendor_name=vendor_name)
        except Vendor.DoesNotExist():
            result = {'error':'資料不存在'}
            return Response(result,status=status.HTTP_404_NOT_FOUND)

        serializer = MyModelSerializer(queryset,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        result = {'error':'更改失敗或資料不存在'}
        return Response(result,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def ClintUse(request):

    if request.method == 'GET':
        vendor_name = request.POST.get('vendor_name')
        queryset = Vendor.objects.filter(vendor_name=vendor_name)
        if queryset.exists():
            serializer = MyModelSerializer(queryset,many=True)
            return Response(serializer.data , status=status.HTTP_200_OK)
        else:
            result = {"status":"查無此筆資料"}
            return Response(result,status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def AdminPost(request):

    if request.method == 'POST':
    
            serializer = MyModelSerializer(data=request.POST)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data , status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        