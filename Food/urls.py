from django.urls import path,include
from .views import Clients , Clients_Check

app_name = 'vendor'
urlpatterns = [
        path('createfoods/', Clients, name='create_foods'),
        path ('foodList/',Clients_Check,name='food_list'),
]