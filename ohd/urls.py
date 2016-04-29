"""ohd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns,include, url



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^tags/(?P<tag>\w+)/$', 'posts.views.tag', name='tagt'),
    url(r'^accounts/',include('allauth.urls')),
    url(r'^$', 'posts.views.home',name='home'),
    url(r'^about/', 'posts.views.about',name='about'),
    url(r'^query/', 'posts.views.querytype',name='query'),
    url(r'^ask_query/admissions/', 'posts.views.admquery',name='admqueryask'),
    url(r'^admissions/queries', 'posts.views.admquerylist',name='admquerylist'),
    url(r'^admissions/querydetail/(?P<id>\d+)/$', 'posts.views.admquerydetail',name='admquerydetail'),
    url(r'^admissions/querydetail/(?P<id>\d+)/edit/$', 'posts.views.admqueryupdate',name='admqueryedit'),
    url(r'^admissions/querydetail/(?P<id>\d+)/delete/$', 'posts.views.admquerydelete',name='admquerydel'),


    url(r'^ask_query/placements/', 'posts.views.plcmntquery',name='plcmntqueryask'),
    url(r'^placements/queries', 'posts.views.plcmntquerylist',name='plcmntquerylist'),
    url(r'^placements/querydetail/(?P<id>\d+)/$', 'posts.views.plcmntquerydetail',name='plcmntquerydetail'),
    url(r'^placements/querydetail/(?P<id>\d+)/edit/$', 'posts.views.plcmntqueryupdate',name='plcmntqueryedit'),
    url(r'^placements/querydetail/(?P<id>\d+)/delete/$', 'posts.views.plcmntquerydelete',name='plcmntquerydel'),


    url(r'^accounts/',include('allauth.urls')),
    url('^markdown/', include( 'django_markdown.urls')),


 


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

