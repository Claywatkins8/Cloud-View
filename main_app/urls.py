from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('map/', views.all_hikes, name='all_hikes'),
    path('hike/<int:hike_id>/', views.hike_show, name='hike_show'),
    path('reports/', views.reports_show, name='reports_show'),
    path('profile/', views.profile, name='profile'),

]
