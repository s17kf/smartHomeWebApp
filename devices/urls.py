from django.urls import path

from . import views

app_name = 'devices'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('location/<int:location_id>/', views.LocationView.as_view(), name='location'),
    path('device/<int:pk>/', views.DeviceView.as_view(), name='device'),
    path('location_update/<int:location_id>', views.location_update, name='location_update'),
]
