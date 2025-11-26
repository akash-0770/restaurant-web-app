"""
URL configuration for resturant project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from Base_App.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',HomeView,name='Home'),
    path('book_table',BookTableView,name='Book_Table'),
    path('menu',MenuView,name='Menu'),
    path('about',AboutView,name='About'),
    path('feedback',FeedbackView,name='Feedback_Form'),
    path('logout',LogoutView,name='logout'),
    path('login/',LoginView.as_view(),name='login'),
    path('signup/',SignupView,name='signup'),
    path('add-to-cart/',add_to_cart,name='add_to_cart'),
    path('cart/', CartPageView.as_view(), name='cart'),
    path('get-cart-items/',get_cart_items,name='get-cart-items'),
    path("increase-qty/", increase_quantity, name="increase-qty"),
    path("decrease-qty/", decrease_quantity, name="decrease-qty"),
    path("delete-cart-item/", delete_cart_item, name="delete-cart-item"),
    path("clear-cart/", clear_cart, name="clear-cart"),



]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
