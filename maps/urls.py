from django.urls import path
from maps import views

urlpatterns = [
    path('map/', views.map_view),
]
