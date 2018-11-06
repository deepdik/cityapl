from django.conf.urls import url
from .views import (	
	test
	)

urlpatterns = [
	# url(r'^$',viewCatsAndSubcats,name="catandsubcats"),
    url(r'^test/$', test, name='test'),
]
