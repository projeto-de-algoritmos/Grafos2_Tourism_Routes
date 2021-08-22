from django.urls import path
from maps import views

urlpatterns = [
    path('attractions/', views.list_attractions, name='list_attractions'),
    path('attractions/select/<str:pk>/', views.select_attraction, name='select_attraction'),
    path('attractions/remove/<str:pk>/', views.remove_attraction, name='remove_attraction'),
    path('map/', views.map_view, name='map_attractions'),
    path('', views.home, name='home'),
    path('test/', views.test, name='test'),
]
