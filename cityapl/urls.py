"""cityapl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from rest_framework_jwt.views import (
    refresh_jwt_token,
    obtain_jwt_token,
    verify_jwt_token
    )
from angulartemplateserver.views import AngularTemplateView
from accounts.views import activate

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^cityapladmin/',include('shop.urls',namespace="shop-admin")),
    url(r'^cityapl/',include('shop.api.urls',namespace="shop-api")),
    url(r'^api/v1/users/',include('accounts.api.urls',namespace="users-api")),
    url(r'^api/chat/',include('chat.api.urls',namespace="chat-api")),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',activate, name='activate'),
    url(r'^api/templates/(?P<item>[A-Za-z0-9\_\.\-\/]+)\.html',AngularTemplateView.as_view()),
#    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # url(r'^auth/', include('rest_framework_social_oauth2.urls')),
    url(r'^api/token/auth/', obtain_jwt_token),
    url(r'^api/token/refresh/', refresh_jwt_token),
    url(r'^api/token/verify/', verify_jwt_token),

    url('^', include('django.contrib.auth.urls')), #email varification
    url(r'^rest-auth/', include('rest_auth.urls')), #social login
    url(r'^accounts/', include('allauth.urls'), name='socialaccount_signup'),
    url(r'', include('chat.urls')),
    # url(r'^ test/' TemplateView.as_view(template_name='an/test.html'))
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    url(r'',TemplateView.as_view(template_name='ang/home.html')),
]
