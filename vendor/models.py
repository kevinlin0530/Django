from django.db import models
from django.contrib import admin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Vendor(models.Model):
	vendor_name = models.CharField(max_length = 20,unique=True,primary_key=True) # 攤販的名稱
	store_name = models.CharField(max_length = 10) # 攤販店家的名稱
	phone_number = models.CharField(max_length = 20) # 攤販的電話號碼
	address = models.CharField(max_length = 100) # 攤販的地址
	vendorList = models.ManyToManyField('self', blank=True)
	def __str__(self):
		return self.vendor_name
	# 如果使用 detailView 就需要這段，需要個別id
	def get_absolute_url(self):
		return reverse("vendors:vendor_id", kwargs={"id": self.id})
@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Vendor._meta.fields] 
    search_fields = ('vendor_name','store_name')