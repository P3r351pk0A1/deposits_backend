from django.http import HttpResponse

from django.shortcuts import render, redirect
from datetime import date
import psycopg2
from .models import  LinkServiceOrder, MiningService, MiningOrder

conn = psycopg2.connect(dbname="mining_services", host="localhost", user="alexandr", password="1111", port="5432")

cursor = conn.cursor()

current_user_id = 1

def getServiceById(ServiceId):
    return MiningService.objects.get(mining_service_id=ServiceId)

def getDraftOrderByIdandUser(OrderId, UserId):
    return MiningOrder.objects.filter(mining_order_id = OrderId, creator_id= UserId, status='draft').first()

def getlinkServiceOrder(OrderId):
    return LinkServiceOrder.objects.filter(mining_order_id=OrderId).all()


def addMiningServiceToCurOrder(UserId, ServiceId, count=1):
    MOrder = MiningOrder.objects.filter(creator_id=current_user_id, status='draft').first() 
    if MOrder == None:
        MOrder = MiningOrder.objects.create(creator_id = UserId, status = 'draft')
    LinkServiceOrder.objects.get_or_create(mining_order_id=MOrder.mining_order_id, mining_service_id=ServiceId, square=777)
    
def DelOrderController(request, id):
    if id!=None:
        cursor.execute('UPDATE mining_order SET status = %s WHERE mining_order_id = %s', ("deleted", id,))
    conn.commit()
    return redirect(MiningServicesController)


def ServiceAddController(request, id):
    MService = getServiceById(id)
    if MService == None:
        return redirect(MiningServicesController)
    addMiningServiceToCurOrder(current_user_id, id)
    return redirect(MiningServicesController)
    
def MiningOrderController(request, id):
    MOrder = getDraftOrderByIdandUser(id, current_user_id)
    if MOrder == None:
        return HttpResponse(status = 404)

    Service_Orders = getlinkServiceOrder(id)
    Mining_Services = []

    for ServiceOrder in Service_Orders:
        MService = getServiceById(ServiceOrder.mining_service_id)
        if MService != None:
            Mining_Services.append({
                'image' : MService.url,
                'name' : MService.name,
                'price' : MService.price
            })

    return render(request, 'mining_order.html', {'data' : {
        'id' : id,
        'miningServices':Mining_Services  
    }})

def MiningServicesController(request):

    MOrderCount = 0
    CurOrderId = -1

    MOrder = MiningOrder.objects.filter(creator_id=current_user_id, status='draft').first()  

    if MOrder!= None:
        Mining_Services_in_current_order = getlinkServiceOrder(MOrder.mining_order_id)
        MOrderCount = len(Mining_Services_in_current_order)
        CurOrderId = MOrder.mining_order_id

    search = ''
    if 'search_mining_service' in request.GET:
        search = request.GET['search_mining_service']

    mining_services_list_main = [] 

    services_found_by_search = MiningService.objects.filter(name__icontains=search)

    for miningService in services_found_by_search:
        isAdded = False
        if MOrder!= None:
            for addedMIningService in Mining_Services_in_current_order:
                if addedMIningService.mining_service_id == miningService.mining_service_id:
                    isAdded = True
                    break
        mining_services_list_main.append({
                    'service_data': miningService,
                    'isAdded': isAdded
                })
    return render(request, 'mining_services.html', {'data' : {
        'miningServices': mining_services_list_main,
        'miningOrderCount' : MOrderCount,
        'miningOrderId' : CurOrderId
        
    }})

def SingleServiceController(request, id):

    miningService = getServiceById(id)    

    if miningService == None:
        return redirect(MiningServicesController)

    return render(request, 'mining_service.html', {'data':{
        'miningService' : miningService
    }})

