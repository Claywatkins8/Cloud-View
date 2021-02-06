from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('map/', views.all_map, name='all_map'),
    path('reports/', views.reports_show, name='reports_show'),

]
