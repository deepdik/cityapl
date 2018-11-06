from django.contrib import admin
from django import forms
from django.contrib.gis.db import models as gis_models
from mapwidgets.widgets import GooglePointFieldWidget
from shop.models import(
	Shop,
	Category,
	SubCategory,
	City,
	Offer,
	FilterTag,
	Feedback,
	ShopRating,
	Vote,
	Pricing,
	)
# Register your models here.


class ShopAdmin(admin.ModelAdmin):
	list_display = ('shopName','pricingTabName','isActive','category','city')
	list_filter = ('isActive','city','category')
	list_editable = ('category','pricingTabName')
	search_fields = ('shopName',)
	formfield_overrides = {
        gis_models.PointField: {"widget": GooglePointFieldWidget}
    }

class PricingAdminForm(forms.ModelForm):
    shop = forms.ModelChoiceField(queryset=Shop.objects.order_by('shopName'))
    class Meta:
        model = Pricing
        fields = '__all__'

class PricingAdmin(admin.ModelAdmin):
	form = PricingAdminForm

admin.site.register(Shop,ShopAdmin)
admin.site.register(Pricing,PricingAdmin)
admin.site.register([Category,SubCategory,FilterTag,City,Offer,Feedback,Vote,ShopRating])