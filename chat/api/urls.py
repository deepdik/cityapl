from django.conf.urls import url
from .views import ( 
MessageListAPIView,
DialogListAPIView,
DialogNotifictionListAPIView,
DialogBlockListAPIView

)

urlpatterns = [
    url(r'^dialogs/(?P<username>[\w.@+-]+)$',MessageListAPIView.as_view(),name="dialogs_detail"),
    url(r'^dialogs/$',DialogListAPIView.as_view(),name="dialogs"),
    url(r'^dialogs/notifications/$',DialogNotifictionListAPIView.as_view(),name="dialogs_notification"),
   	url(r'^dialogs/(?P<username>[\w.@+-]+)/(?P<status>[\w.@+-]+)/$',DialogBlockListAPIView.as_view(),name="dialogs_block"),
   	
]
