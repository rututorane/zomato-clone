from django.conf import settings
from django.conf.urls.static import static
"""
URL configuration for FoodProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.views.generic import TemplateView
from food_app import views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('add-to-Wishlist/<int:item_id>/',views.add_to_Wishlist,name='add_to_Wishlist'),
    path('my_wishlist/',views.wishlist_page,name='wishlist_page'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart,name='add_to_cart'),
    path('my_cart/', views.cart_page, name='cart_page'),
    path('remove-item/<int:item_id>/',views.remove_from_cart, name='remove_item'),
    path('delete-item/<int:item_id>/', views.delete_cart_item, name='delete_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('signup/',views.signup_view, name='signup'),
    path('login/',views.login_view, name='login'),
    path('logout/',views.logout_view, name='logout'),
    path('my_orders/',views.my_orders_view, name='my_orders'),
    path('upi-payment/', TemplateView.as_view(template_name='upi_payment.html'),name='upi_payment'),
    path('order-success/', views.order_success,name='order_success'),
    path('track-order/<int:order_id>/', views.track_order,name='track_order'),
    path('item/<int:item_id>/', views.food_detail, name='food_detail'),
    path('save-rating/<int:item_id>/', views.save_rating, name='save_rating'),
    path('profile/', views.view_profile, name='view_profile'),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)