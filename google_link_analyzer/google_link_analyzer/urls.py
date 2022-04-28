"""google_link_analyzer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
# from google_link import views
from google_link.views import *




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', load_google_link, name='loadlink'),
    path('', scrapped_list, name='scrappedapi-detail'),
    path('api/delete/', delete_google_link, name='deletelink'),
    path('api/update/', update_web_link, name='updatelink'),
]
