from django.db import models
from vendor.models import Vendor
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
# Create your models here.
class Food(models.Model):
    food_name = models.CharField(max_length = 30) # 食物名稱
    price = models.DecimalField(max_digits = 3, decimal_places=0) # 食物價錢
    #! 如果foreignkey 要指定vendor_name 加入參數 (to_field='vendor_name')
    food_vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,to_field='vendor_name',related_name='food_foods') # 代表這食物是由哪一個攤販所做的

    def __str__(self):
        return self.food_name
    
class Morethanfifty(admin.SimpleListFilter):

	title = _('price')
	parameter_name = 'compareprice' # url最先要接的參數

	def lookups(self, request, model_admin):
		return (
			('>50',_('>50')), # 前方對應下方'>50'(也就是url的request)，第二個對應到admin顯示的文字
			('<=50',_('<=50')),
			('>=100',_('>=100')),
		)
    # 定義查詢時的過濾條件
	def queryset(self, request, queryset):
		if self.value() == '>50':
			return queryset.filter(price__gt=50)
		if self.value() == '<=50':
			return queryset.filter(price__lte=50)
		if self.value() == '>=100':
			return queryset.filter(price__gte=100)

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Food._meta.fields]
	list_filter = (Morethanfifty,)
	search_fields = ('food_name','price')
	ordering = ('price',)