from django.shortcuts import render
import psycopg2
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from deposits_app.serializers import *
from deposits_app.models import *
from .minio import *
from django.utils import timezone
import datetime
from django.contrib.auth import get_user_model

conn = psycopg2.connect(dbname="mining_services", host="localhost", user="alexandr", password="1111", port="5432")


#переделать по етоде
def user():
    try:
        user1 = AuthUser.objects.get(id=1)
    except:
        user1 = AuthUser(id = 1, first_name = "Александр", last_name = "Пересыпко", password = 1111, username = "user1")
    return user1

class MiningServiceMethods(APIView):
    model_class = MiningService
    serializer_class = MiningServiceSerializer

    #GET получить список услуг с фильтрацией, ид заявки и кол-во услуг в ней
    def get (self, request, format = None):
        searchingMiningServices = request.query_params.get('name')

        filteredMiningServices = self.model_class.objects.filter(status = 'valid')
        if searchingMiningServices:
            filteredMiningServices = MiningService.objects.filter(name__icontains=searchingMiningServices)
            
        CurUser = user()
        if CurUser:
            UsersDraft = MiningOrder.objects.filter(creator_id=CurUser.id, status='draft').first()
        if UsersDraft:
            UsersDraftId = UsersDraft.mining_order_id
            MiningServicesInUsersDraft = LinkServicesOrders.objects.filter(mining_order_id = UsersDraftId).count()
            
        else:
            MiningServicesInUsersDraft = 0
            UsersDraftId = 0
        serializer = self.serializer_class(filteredMiningServices, many = True)
        return Response({'Services':serializer.data, 
                         'MiningServicesInUsersDraft':MiningServicesInUsersDraft,
                          'UsersDraftId': UsersDraftId})
    
    #POST добавление услуги без изображения
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
    def put(self, request, pk, format = None):
        Mining_Service = get_object_or_404(self.model_class, pk=pk)
        serializer = self.serializer_class(Mining_Service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #DELETE удаление услуги вместе с изображением
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
    def post(self, request, pk, format = None):
        CurUser = user()
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
    serializer_class = MiningService

    #POST Добавление изображения по id услуги
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
    def get(self, request, format = None):
        MiningOrderDateFormed = request.query_params.get('date_formed')
        MiningOrderStatus  = request.query_params.get('status')

        filters = {}
        if MiningOrderDateFormed: 
            filters['formation_date'] = MiningOrderDateFormed
        if MiningOrderStatus:
            filters['status'] = MiningOrderStatus

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
    def get(self, request, pk, format = None):
        Mining_Order = get_object_or_404(self.model_class, pk=pk)
        
        if Mining_Order:
            serializer = self.serializer_class(Mining_Order)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data)
    
    #put изменение полей заявки
    def put(self, request, pk, format = None):
        Mining_Order = get_object_or_404(self.model_class, pk=pk)
        if Mining_Order.status != 'draft' and Mining_Order.status != 'formed':
            return Response({'error':'This order is deleted or already moderated'})
        serializer = MiningOrdermmfieldsSerializer(Mining_Order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #delete удаление
    def delete(self, request, pk, format = None):
        Mining_Order = get_object_or_404(self.model_class, pk=pk)
        Mining_Order.status='deleted'
        Mining_Order.save()
        serializer = self.serializer_class(Mining_Order)
        return Response(serializer.data)
    
class FormingByCreator(APIView):
    model_class = MiningOrder
    serializer_class = SingleMiningOrderSerializer

    #put сформировать создателем
    def put(self, request, pk, format = None):
        Mining_Order = get_object_or_404(self.model_class, pk=pk)
        serializer = self.serializer_class(Mining_Order)
        if Mining_Order.status == 'draft' and Mining_Order.company_name is not None and Mining_Order.location is not None and Mining_Order.mining_start_date is not None:
            Mining_Order.formation_date = datetime.date.today().isoformat()
            Mining_Order.status = 'formed'
            Mining_Order.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response({'ERROR': 'some required fields were not declared or its not draft'}, status=status.HTTP_400_BAD_REQUEST)

class AcceptOrDenyByModerator(APIView):
    model_class = MiningOrder
    serializer_class = SingleMiningOrderSerializer

    #put модерация
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

        Mining_Order.order_cost = Mining_order_price
        Mining_Order.moderation_date = datetime.date.today().isoformat()
        Mining_Order.moderator_id = user().id
        Mining_Order.save()

        serializer = SingleMiningOrderSerializer(Mining_Order)
        return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
    
class LinkMiningServisesOrdersMethods(APIView):
    model_class = LinkServicesOrders
    serializer_class = MiningServiceOrderSerializer

    #delete удаление из заявки
    def delete(self, request, pk_mservice, pk_morder, format = None):
        MiningServise_link = get_object_or_404(self.model_class, mining_order = pk_morder, mining_service = pk_mservice)
        if MiningServise_link:
            MiningServise_link.delete()
        MiningService_list = self.model_class.objects.filter(mining_order=pk_morder)
        return Response(self.serializer_class(MiningService_list, many=True).data, status=status.HTTP_202_ACCEPTED)
 
    #put изменение полей в м-м
    def put(self, request, pk_mservice, pk_morder, format = None):
        MiningServise_link = get_object_or_404(self.model_class, mining_order = pk_morder, mining_service = pk_mservice)
        serializer = self.serializer_class(MiningServise_link, data = {'square':request.query_params.get('square')})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserMethods(APIView):
    model_class = get_user_model()
    serializer_class = AuthUserSerializer

    #post регистрация
    def post(self, request, format = None):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            new_user = self.model_class.objects.create_user(
                username = serializer.validated_data.get('username'),
                password = serializer.validated_data.get('password'),
                is_superuser = serializer.validated_data.get('is_superuser'),
                is_staff = serializer.validated_data.get('is_staff'),
                email = serializer.validated_data.get('email'),
                first_name = serializer.validated_data.get('first_name'),
                last_name = serializer.validated_data.get('last_name'),
                date_joined = datetime.date.today().isoformat()
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #put пользовотеля (ЛК)
    def put(self, request, pk, format = None):
        edited_user = get_object_or_404(self.model_class, pk=pk)
        serializer = self.serializer_class(edited_user, data=request.query_params, partial=True)
        pw = request.query_params.get('password')
        if serializer.is_valid():
            if 'password' in serializer.validated_data:
                edited_user.set_password(serializer.validated_data.get('password'))
                edited_user.save()
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class Authentification(APIView):
    model_class = get_user_model()
    serializer_class = AuthUserSerializer
    
    #post аутентификация
    def post(self, request, format = None):
        # cur_user = self.model_class.objects.get(pk=pk)
        inp_password = request.query_params.get('password')
        inp_username = request.query_params.get('username')
        cur_user = self.model_class.objects.get(username=inp_username)
        if cur_user.check_password(inp_password):
            return Response({'authentification':'success'}, status=status.HTTP_200_OK)
        return Response({'authentification':'failed'}, status=status.HTTP_400_BAD_REQUEST)

class Deauthorisation(APIView):
    model_class = get_user_model()
    serializer_class = AuthUserSerializer
    
    #post деавторизация
    def post(self, request, format = None):
        return Response({'deauthorisation':'complete'}, status=status.HTTP_401_UNAUTHORIZED)

