from django.http import HttpResponse
import os
from django.shortcuts import render
from .models import (
	Category,
	SubCategory,
	FilterTag
	)


from django.template import loader

# Create your views here.

# def addCity(request):
# 	return render(request,'shop/addCityTemplate.html',{})

# def viewCatsAndSubcats(request):
# 	categories = Category.objects.order_by('name')
# 	subCategories = SubCategory.objects.order_by('name')
# 	context = {
# 		'categories':categories,
# 		'subCategories':subCategories
# 	}
# 	return render(request,'shop/viewCat.html',context)

def test(request):


	def list_files(startpath):
	    for root, dirs, files in os.walk(startpath):
	        level = root.replace(startpath, '').count(os.sep)
	        indent = ' ' * 4 * (level)
	        print('{}{}/'.format(indent, os.path.basename(root)))
	        subindent = ' ' * 4 * (level + 1)
	        for f in files:
	            print('{}{}'.format(subindent, f))
					
	c = list_files('/home/deepak/cityapl/static')
	
				
	context = {
		'test' :c
	
	}
	return render(request, "test.html", context)