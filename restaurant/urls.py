from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('book/', views.book, name="book"),
    path('api/reservations/', views.bookingsApi, name="reservations"),
    path('menu/', views.menu, name="menu"),
    path('api/menu/', views.menuApi, name="menu"),
    path('api/menu/<int:id>/', views.menu_item, name="menu_item"),  
    path('bookings', views.bookings, name='bookings'), 
]