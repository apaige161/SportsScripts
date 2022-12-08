"""sportsApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from sportsApp import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('players/', views.player_list),
    # path('players/<int:id>/', views.player_detail_plus), # example of cRUD, do not actually use this for sports app 
    path('players/<int:id>', views.player_detail),
    path('addPlayer/', views.add_player)
]

# allow json to be viewed in the JSON
urlpatterns = format_suffix_patterns(urlpatterns)