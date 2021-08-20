from django.urls import path
from maps import views

urlpatterns = [
    path('attractions/', views.select_attraction, name='list_attractions'),
    path('delete/<str:pk>/', views.cancel_attraction, name='delete_attraction'),
    path('map/', views.map_view),
]
