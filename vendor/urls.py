
from django.urls import path,include
from .views import VendorListView , ClintUse,AdminPost

app_name = 'vendor'
urlpatterns = [
        path('', VendorListView.as_view(), name='vendor_list'),
        path('vendorList/',ClintUse,name ='vendor_list_clint' ),
        path('AdminPost/',AdminPost,name = 'admin_post'),

]