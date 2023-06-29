"""booking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from app import views
from django.conf import settings 
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('signin/', views.signin, name='signin'),
    path('', views.index, name=''),
    path('add_hotel', views.add_hotel, name='add_hotel'),
    path('profile', views.profile, name='profile'),
    path('profile_edit', views.profile_edit, name='profile_edit'),
    path('details/<int:pk>/', views.hotel_detail, name='detail'),
    path('delete/<int:pk>/', views.delete_hotel, name='delete'),
    path('update/<int:pk>/', views.update_hotel, name='update'),
    path("logout_user", views.logout, name="logout"),
    path('search/', views.search_hotel, name='search'),
    path('add_to_cart/<int:hotel_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:hotel_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart, name='cart'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('book/<int:pk>/', views.book_hotel, name='book_hotel'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
