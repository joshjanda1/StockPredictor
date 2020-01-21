"""stockpredictor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url, include
from stocks.views import detail_view
from stocks import views
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'home/', views.index, name='index'),
	url(r'detail_view/', detail_view, name='detail_view'),
    url(r'random_view/', views.random_view, name='random_view'),
    url(r'about/', views.about, name='about'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
