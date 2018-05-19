"""scraper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf.urls import url
from django.views.generic import RedirectView

from chair.views import *

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='console/', permanent=False)),
    url(r'^console/$', console, name='console'),
    url(r'^orders/grab_latest/$', grab_latest_orders, name='grab_latest_orders'),
    url(r'^orders/newegg_fulfill/(?P<order_id>[-_a-zA-Z0-9]+)/$', newegg_fulfill, name='newegg_fulfill'),
    url(r'^orders/update_tracking/(?P<order_id>[-_a-zA-Z0-9]+)/$', update_tracking, name='update_tracking'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]
