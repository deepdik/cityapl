import os

from django.conf import settings
from django.http import HttpResponse,Http404

from django.views.generic import View
from django.shortcuts import render

class AngularTemplateView(View):
	def get(self,request,item=None,*args,**kwargs):
		template_path  = settings.TEMPLATES[0]["DIRS"][0]
		path = os.path.join(template_path,"ang","app",item+".html")
		print(path)
		try:
			html = open(path)
			return HttpResponse(html)
		except:
			raise Http404
	
