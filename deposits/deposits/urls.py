from django.contrib import admin
from deposits_app import views
from django.urls import include, path
from rest_framework import permissions, routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r'user', views.UserRegistration, basename='user')

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('user/login',  views.Authentication.as_view(), name='login'),
    path('user/logout', views.Deauthorisation.as_view(), name='logout'),  
    path('user/reg', views.UserRegistration.as_view(), name = 'mining-user'),
    path('user/<int:pk>', views.UserRegistration.as_view(), name = 'mining-user-lk'),

    path('admin/', admin.site.urls),
    # path('', include(router.urls)),

    path('miningServices', views.MiningServiceMethods.as_view(), name='mining-services'),
    path('miningServices/<int:pk>', views.MiningServiceMethods_byId.as_view(), name='single-mining-service'),
    path('miningServices/<int:pk>/add_mining_img', views.MiningServiceImageUpload.as_view(), name='add-mining-img'),

    path('miningOrders', views.MiningOrdersMethods.as_view(), name = 'mining-orders'),
    path('miningOrders/<int:pk>', views.MiningOrderMethods_byId.as_view(), name = 'mining-orders'),
    path('miningOrders/<int:pk>/forming', views.FormingByCreator.as_view(), name = 'mining-orders-forming'),
    path('miningOrders/<int:pk>/moderating', views.AcceptOrDenyByModerator.as_view(), name = 'mining-orders-moderating'),

    path('miningServiceOrder/<int:pk_mservice>/<int:pk_morder>', views.LinkMiningServisesOrdersMethods.as_view(), name = 'mining-service-orders'),
    
    # path(r'miningUser', views.UserMethods.as_view(), name = 'mining-user'),
    # path(r'miningUser/<int:pk>', views.UserMethods.as_view(), name = 'mining-user-pw'),

    # path(r'authentification', views.Authentification.as_view(), name = 'mining-user-authentification'),
    # path(r'deauthorisation', views.Deauthorisation.as_view(), name = 'mining-user-deauthorisation'),

    
   
   

]