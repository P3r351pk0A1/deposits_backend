from deposits_lab import views
from django.urls import path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('basket/<int:id>', views.BasketController, name='basket_url'),
    path('', views.OrdersController, name = 'main_url'),
    path('order/<int:id>/', views.SingleOrderController, name='order_url'),
]