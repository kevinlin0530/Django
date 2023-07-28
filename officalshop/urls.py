"""
URL configuration for officalshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path , include
from rest_framework.routers import DefaultRouter
from vendor.views import VendorList
from Food.views import FoodModel
from django.views.generic.base import TemplateView
from django.urls import path , include

vendor_router = DefaultRouter()
vendor_router.register(r'vendor',VendorList )

food_router = DefaultRouter()
food_router.register(r'food',FoodModel)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api_vendor/',include(vendor_router.urls)),
    path('api_food/',include(food_router.urls)),
    path('food/',include('Food.urls',namespace='create_food')),
    path('vendor/',include('vendor.urls',namespace='vendor_list')),
]
