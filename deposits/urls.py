from deposits import views
from django.urls import path
from django.contrib import admin
from .views import MiningOrderController, MiningServicesController, SingleServiceController, ServiceAddController

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mining_ordder/<int:id>', views.MiningOrderController, name='mining_order_url'),
    path('', views.MiningServicesController, name = 'main_url'),
    path('smining_service/<int:id>/', views.SingleServiceController, name='mining_service_url'),
    path('add/<int:id>', views.ServiceAddController, name = 'add_service_url'),
    path('del/<int:id>', views.DelOrderController, name = 'del_order_url'),
    
]