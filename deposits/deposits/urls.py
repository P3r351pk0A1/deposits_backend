from django.contrib import admin
from deposits_app import views
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),

    path(r'miningServices', views.MiningServiceMethods.as_view(), name='mining-services'),
    path(r'miningServices/<int:pk>', views.MiningServiceMethods_byId.as_view(), name='single-mining-service'),
    path(r'miningServices/<int:pk>/add_mining_img', views.MiningServiceImageUpload.as_view(), name='add-mining-img'),

    path(r'miningOrders', views.MiningOrdersMethods.as_view(), name = 'mining-orders'),
    path(r'miningOrders/<int:pk>', views.MiningOrderMethods_byId.as_view(), name = 'mining-orders'),
    path(r'miningOrders/<int:pk>/forming', views.FormingByCreator.as_view(), name = 'mining-orders-forming'),
    path(r'miningOrders/<int:pk>/moderating', views.AcceptOrDenyByModerator.as_view(), name = 'mining-orders-moderating'),

    path(r'miningServiceOrder/<int:pk_mservice>/<int:pk_morder>', views.LinkMiningServisesOrdersMethods.as_view(), name = 'mining-service-orders'),
    
    path(r'miningUser', views.UserMethods.as_view(), name = 'mining-user'),
    path(r'miningUser/<int:pk>', views.UserMethods.as_view(), name = 'mining-user-pw'),

    path(r'authentification', views.Authentification.as_view(), name = 'mining-user-authentification'),
    path(r'deauthorisation', views.Deauthorisation.as_view(), name = 'mining-user-deauthorisation'),

    
   
   

]