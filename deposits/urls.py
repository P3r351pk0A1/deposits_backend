from deposits import views
from django.urls import path
from django.contrib import admin
from .views import BasketController, OrdersController, SingleOrderController, OrderAddController

urlpatterns = [
    path('admin/', admin.site.urls),
    path('basket/<int:id>', views.BasketController, name='basket_url'),
    path('', views.OrdersController, name = 'main_url'),
    path('order/<int:id>/', views.SingleOrderController, name='order_url'),
    path('add/<int:id>', views.OrderAddController, name = 'addOrder_url'),
    path('del/<int:id>', views.DelBasketController, name = 'delBasket_url'),
    
]