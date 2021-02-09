from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('map/', views.all_hikes, name='all_hikes'),
    path('profile/', views.profile, name='profile'),
    path('reports/', views.reports_all, name='reports_all'),
    path('reports/<int:report_id>/', views.reports_show, name='reports_show'),
    path('reports/<int:report_id>/edit/',
         views.reports_edit, name='reports_edit'),
    path('reports/<int:report_id>/<int:hike_id>/delete/',
         views.report_delete, name='report_delete'),
    path('hike/<int:hike_id>/', views.hike_show, name='hike_show'),
    path('hike/<int:hike_id>/create/', views.report_create, name='report_create'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
