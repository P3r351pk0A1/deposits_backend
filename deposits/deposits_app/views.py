from django.shortcuts import render
import psycopg2
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from deposits_app.serializers import *
from deposits_app.models import *
from .minio import *
from django.utils import timezone
import datetime
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
import redis
import uuid
from deposits_app.permissions import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .getUserBySession import getUserBySession

conn = psycopg2.connect(dbname="mining_services", host="localhost", user="alexandr", password="1111", port="5432")

session_storage = redis.StrictRedis(host = settings.REDIS_HOST, port = settings.REDIS_PORT)

def method_permission_classes(classes):
    def decorator(func):
        def decorated_func(self, *args, **kwargs):
            self.permission_classes = classes
            user = getUserBySession(self.request)
            if user == AnonymousUser():
                return Response({"detail": "Authentication credentials were not providedsss."}, status=401)
            else:
                try:
                    self.check_permissions(self.request)
                except Exception as e:
                    return Response({"detail": "You do not have permission to perform this action."}, status=403)
            return func(self, *args, **kwargs)
        return decorated_func
    return decorator

class MiningServiceMethods(APIView):
    model_class = MiningService
    serializer_class = MiningServiceSerializer

    #GET получить список услуг с фильтрацией, ид заявки и кол-во услуг в ней

    def get (self, request, format = None):
        searchingMiningServices = request.query_params.get('name')


        filteredMiningServices = self.model_class.objects.filter(status = 'valid')
        if searchingMiningServices:
            filteredMiningServices = MiningService.objects.filter(name__icontains=searchingMiningServices)

        CurUser = getUserBySession(self.request)
        if CurUser != AnonymousUser():
            UsersDraft = CurUser.UserMiningOrders.filter(status='draft').first()
            if UsersDraft:
                UsersDraftId = UsersDraft.mining_order_id
                MiningServicesInUsersDraft = LinkServicesOrders.objects.filter(mining_order_id = UsersDraftId).count()
            else:
                MiningServicesInUsersDraft = 0
                UsersDraftId = 0
        else:
            MiningServicesInUsersDraft = 0
            UsersDraftId = 0
        serializer = self.serializer_class(filteredMiningServices, many = True)
        return Response({'Services':serializer.data, 
                         'MiningServicesInUsersDraft':MiningServicesInUsersDraft,
                          'UsersDraftId': UsersDraftId})
    
    #POST добавление услуги без изображения
    @swagger_auto_schema(request_body = serializer_class)
    @method_permission_classes([IsAdmin])
    def post(self, request, format = None):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MiningServiceMethods_byId(APIView):
    model_class = MiningService
    serializer_class = MiningServiceSerializer

    #GET получение одной услуги
    def get (self, request, pk, format = None):
        Mining_Service = get_object_or_404(self.model_class, pk=pk)
        serializer = self.serializer_class(Mining_Service)
        return Response(serializer.data)
    
    #PUT изменение услуги
    @swagger_auto_schema(request_body = serializer_class)
    @method_permission_classes((IsAdmin,))
    def put(self, request, pk, format = None):
        Mining_Service = get_object_or_404(self.model_class, pk=pk)
        serializer = self.serializer_class(Mining_Service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #DELETE удаление услуги вместе с изображением
    @method_permission_classes((IsAdmin,))
    def delete(self, request, pk, format = None):
        Mining_Service = get_object_or_404(self.model_class, pk=pk)
        result = del_pic(Mining_Service)
        if 'error' in result.data:
            return result
        Mining_Service.delete()
        MiningServiceInOrders = LinkServicesOrders.objects.filter(mining_service_id = Mining_Service.mining_service_id)
        if MiningServiceInOrders:
            MiningServiceInOrders.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    #Post добавление услуги в черновик
    @swagger_auto_schema(request_body = MiningOrdersSerialiser)
    @method_permission_classes([IsAuth])
    def post(self, request, pk, format = None):
        CurUser = getUserBySession(request)
        draftOrder = CurUser.UserMiningOrders.filter(status = 'draft').first()
        Mining_Service = get_object_or_404(self.model_class, pk=pk)
        if not draftOrder :
            draftOrder = MiningOrder(creator = CurUser, status = 'draft')
            draftOrder.save()
        if not LinkServicesOrders.objects.filter(mining_order_id = draftOrder.mining_order_id, mining_service_id = Mining_Service.mining_service_id).exists():
            Mining_Service_link = LinkServicesOrders(mining_order_id = draftOrder.mining_order_id, mining_service_id = Mining_Service.mining_service_id)
            Mining_Service_link.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_208_ALREADY_REPORTED)
        

class MiningServiceImageUpload(APIView):
    model_class = MiningService
    serializer_class = MiningServiceSerializer

    #POST Добавление изображения по id услуги
    @swagger_auto_schema(request_body = serializer_class)
    @method_permission_classes((IsAdmin,))
    def post(self, request, pk, format=None):
        Mining_service = get_object_or_404(self.model_class, pk=pk)
        mining_pic = request.FILES.get('mining_pic')
        mining_pic_result = add_pic(Mining_service, mining_pic)
        if 'error' in mining_pic_result.data:
            return mining_pic_result
        return Response(status=status.HTTP_201_CREATED)

class MiningOrdersMethods(APIView):
    model_class = MiningOrder
    serializer_class = MiningOrdersSerialiser

    #GET список с фильтрацией по диапозону даты формирования и статусу
    @method_permission_classes([IsAuth])
    def get(self, request, format = None):
        CurUser = getUserBySession(request)
        MiningOrderDateFormed = request.query_params.get('date_formed')
        MiningOrderStatus  = request.query_params.get('status')

        filters = {}
        if MiningOrderDateFormed: 
            filters['formation_date'] = MiningOrderDateFormed
        if MiningOrderStatus:
            filters['status'] = MiningOrderStatus
        if not (CurUser.is_staff or CurUser.is_superuser):
            filters['creator'] = CurUser

        Mining_Orders = self.model_class.objects.filter(**filters).exclude(Q(status = 'draft') | Q(status = 'deleted'))
        if Mining_Orders:
            serializer = self.serializer_class(Mining_Orders, many = True) 
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data)
    
class MiningOrderMethods_byId(APIView):
    model_class = MiningOrder
    serializer_class = SingleMiningOrderSerializer
    
    #get одна запись - список услуг с картинками
    @method_permission_classes([IsAuth])
    def get(self, request, pk, format = None):
        CurUser = getUserBySession(request)
        if not (CurUser.is_staff or CurUser.is_superuser):
            Mining_Order = get_object_or_404(self.model_class, pk=pk, creator = CurUser)
        else: 
            Mining_Order = get_object_or_404(self.model_class, pk=pk)

        if Mining_Order:
            serializer = self.serializer_class(Mining_Order)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data)

    #put изменение полей заявки
    @method_permission_classes([IsAuth])
    @swagger_auto_schema(request_body = serializer_class)
    def put(self, request, pk, format = None):
        CurUser = getUserBySession(request)
        if not (CurUser.is_staff or CurUser.is_superuser):
            Mining_Order = get_object_or_404(self.model_class, pk=pk, creator = CurUser)
        else: 
            Mining_Order = get_object_or_404(self.model_class, pk=pk)

        if Mining_Order.status != 'draft' and Mining_Order.status != 'formed':
            return Response({'error':'This order is deleted or already moderated'})
        serializer = MiningOrdermmfieldsSerializer(Mining_Order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #delete удаление
    @method_permission_classes([IsAuth])
    def delete(self, request, pk, format = None):
        CurUser = getUserBySession(request)
        if not (CurUser.is_staff or CurUser.is_superuser):
            Mining_Order = get_object_or_404(self.model_class, pk=pk, creator = CurUser)
        else: 
            Mining_Order = get_object_or_404(self.model_class, pk=pk)

        Mining_Order.status='deleted'
        Mining_Order.save()
        serializer = self.serializer_class(Mining_Order)
        return Response(serializer.data)
    
class FormingByCreator(APIView):
    model_class = MiningOrder
    serializer_class = SingleMiningOrderSerializer

    #put сформировать создателем
    @method_permission_classes([IsAuth])
    @swagger_auto_schema(request_body = serializer_class)
    def put(self, request, pk, format = None):
        CurUser = getUserBySession(request)
        Mining_Order = get_object_or_404(self.model_class, pk=pk)
        serializer = self.serializer_class(Mining_Order)
        print(serializer)
        if Mining_Order.creator == CurUser and Mining_Order.status == 'draft' and Mining_Order.company_name is not None and Mining_Order.location is not None and Mining_Order.mining_start_date is not None:
            Mining_Order.formation_date = datetime.date.today().isoformat()
            Mining_Order.status = 'formed'
            Mining_Order.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response({'ERROR': 'some required fields were not declared or its not draft'}, status=status.HTTP_400_BAD_REQUEST)

class AcceptOrDenyByModerator(APIView):
    model_class = MiningOrder
    serializer_class = SingleMiningOrderSerializer

    #put модерация
    @method_permission_classes([IsManager])
    @swagger_auto_schema(request_body = serializer_class)
    def put(self, request, pk, format = None):
        IsMiningOrderAccepted = request.query_params.get('ModeratorAccepted')
        Mining_Order = get_object_or_404(self.model_class, pk=pk)
        if  Mining_Order.status != 'formed':
            return Response({'error': 'Mining order is not formed'})
        if IsMiningOrderAccepted == '1':
            Mining_Order.status = 'accepted'
        else:
            Mining_Order.status = 'denied'
        
        services_in_current_OrderLnk = LinkServicesOrders.objects.filter(mining_order = Mining_Order.mining_order_id)
        services_in_current_Order = []
        for MserviceLnk in services_in_current_OrderLnk:
            if MserviceLnk.mining_service:
                services_in_current_Order.append(MserviceLnk.mining_service)

        #считаем полную стоимость заказа
        Mining_order_price = 0
        for MService in services_in_current_Order:
            Mining_order_price += MService.price

        Mining_Order = MiningOrder(order_cost = Mining_order_price, 
                                   moderation_date = datetime.date.today().isoformat(),
                                   moderator_id = getUserBySession(request).id)
        Mining_Order.save()

        serializer = SingleMiningOrderSerializer(Mining_Order)
        return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
    
class LinkMiningServisesOrdersMethods(APIView):
    model_class = LinkServicesOrders
    serializer_class = MiningServiceOrderSerializer

#каждому юзеру - свои заявки?#каждому юзеру - свои заявки?#каждому юзеру - свои заявки?#каждому юзеру - свои заявки?#каждому юзеру - свои заявки?    

    #delete удаление из заявки
    @method_permission_classes([IsAuth])
    def delete(self, request, pk_mservice, pk_morder, format = None):
        CurUser = getUserBySession(request)
        if not (CurUser.is_staff or CurUser.is_superuser):
            Mining_Order = get_object_or_404(self.model_class, pk=pk_morder, creator = CurUser)
        else: 
            Mining_Order = get_object_or_404(self.model_class, pk=pk_morder)

        MiningServise_link = get_object_or_404(self.model_class, mining_order = Mining_Order, mining_service = pk_mservice)
        if MiningServise_link:
            MiningServise_link.delete()
        MiningService_list = self.model_class.objects.filter(mining_order=pk_morder)
        return Response(self.serializer_class(MiningService_list, many=True).data, status=status.HTTP_202_ACCEPTED)

#каждому юзеру - свои заявки?#каждому юзеру - свои заявки?#каждому юзеру - свои заявки?#каждому юзеру - свои заявки?#каждому юзеру - свои заявки?    

    #put изменение полей в м-м
    @method_permission_classes([IsAuth])
    @swagger_auto_schema(request_body = serializer_class)
    def put(self, request, pk_mservice, pk_morder, format = None):
        MiningServise_link = get_object_or_404(self.model_class, mining_order = pk_morder, mining_service = pk_mservice)
        serializer = self.serializer_class(MiningServise_link, data = {'square':request.query_params.get('square')})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRegistration(APIView):
    model_class = get_user_model()
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]

    #post регистрация
    @swagger_auto_schema(request_body = serializer_class)
    def post(self, request, format = None):
        CurUser = getUserBySession(request)
        if self.model_class.objects.filter(email=request.data['username']).exists():
            return Response({'status': 'Exist'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            self.model_class.objects.create_user(username=serializer.validated_data['username'],
                                     password=serializer.validated_data['password'],
                                     is_superuser=serializer.validated_data['is_superuser'],
                                     is_staff=serializer.validated_data['is_staff'],
                                     email = serializer.validated_data['email'],
                                     )  
            if CurUser.is_staff or CurUser.is_superuser:
                userList = self.model_class.objects.all()    
                return Response(self.serializer_class(userList, many = True), status=200)
            return Response({'status': 'Success'}, status=200)
        return Response({'status': 'Error', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    #put пользовотеля (ЛК)
    @swagger_auto_schema(request_body = serializer_class)
    def put(self, request, pk, format = None):
        edited_user = get_object_or_404(self.model_class, pk=pk)
        serializer = self.serializer_class(edited_user, data=request.query_params, partial=True)
        if serializer.is_valid():
            if 'password' in serializer.validated_data:
                edited_user.set_password(serializer.validated_data.get('password'))
                edited_user.save()
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class Authentication(APIView):
    model_class = get_user_model()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    
    #post аутентификация
    @swagger_auto_schema(request_body = serializer_class)
    def post(self, request, format = None):
        # cur_user = self.model_class.objects.get(pk=pk)
        inp_password = request.data['password']
        inp_username = request.data['username']
        cur_user = authenticate(request, username = inp_username, password = inp_password)
        if cur_user != None:
            randKey = str(uuid.uuid4())
            print(randKey)
            session_storage.set(randKey, inp_username)

            old_session_id = request.COOKIES.get('session_id', '')
            if old_session_id:
                if session_storage.get(old_session_id):
                    session_storage.delete(old_session_id)

            resp = HttpResponse("{'status':'ok'}")
            resp.set_cookie("session_id", randKey)
            return resp
        else: 
            return HttpResponse("{'authentification':'failed'}", status=status.HTTP_400_BAD_REQUEST)
        

class Deauthorisation(APIView):
    model_class = get_user_model()
    serializer_class = UserSerializer
    permission_classes = [IsAuth]
    
    #post деавторизация
    @swagger_auto_schema(request_body = serializer_class)
    def post(self, request, format = None):
        sess_id = request.COOKIES.get('session_id')
        session_storage.delete(sess_id)
        return Response({'deauthorisation':'complete'}, status=status.HTTP_401_UNAUTHORIZED)
