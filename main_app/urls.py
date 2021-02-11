from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('map/', views.all_hikes, name='all_hikes'),
    path('profile/', views.profile, name='profile'),
    path('profile/add_user_photo/',
         views.add_user_photo, name='add_user_photo'),
    path('profile/<int:photo_id>/delete/',
         views.user_photo_delete, name='user_photo_delete'),
    path('reports/add_report_photo/<int:report_id>/',
         views.add_report_photo, name='add_report_photo'),
    path('reports/<int:photo_id>/delete/',
         views.report_photo_delete, name='report_photo_delete'),
    path('reports/', views.reports_all, name='reports_all'),
    path('reports/<int:report_id>/', views.reports_show, name='reports_show'),
    path('reports/<int:report_id>/edit/',
         views.reports_edit, name='reports_edit'),
    path('reports/<int:report_id>/<int:hike_id>/delete/',
         views.report_delete, name='report_delete'),
    path('hike/<int:hike_id>/', views.hike_show, name='hike_show'),
    path('hike/<int:hike_id>/create/', views.report_create, name='report_create'),
    path('hike/<int:hikePhoto_id>/add_hike_photo/',
         views.hikePhoto, name='hikePhoto'),
    path('hike/<int:photo_id>/delete/',
         views.hike_photo_delete, name='hike_photo_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
