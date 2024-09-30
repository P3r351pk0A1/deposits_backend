from django.shortcuts import render, redirect
from datetime import date
import psycopg2
from .models import  LinkBasketOrder, MiningBasket, MiningOrder, User

conn = psycopg2.connect(dbname="Mining_services", host="localhost", user="alexandr", password="1111", port="5432")

cursor = conn.cursor()

current_user_id = 1

def getOrderById(Order_id):
    return MiningOrder.objects.get(order_id=Order_id)

def getDraftBasketByIdandUser(BasketId, UserId):
    return MiningBasket.objects.get(basket_id = BasketId, creator_id= UserId, status='draft')

def getlinkBasketOrders(BasketId):
    return LinkBasketOrder.objects.filter(basket_id=BasketId).all()


def addOrderToCurBasket(User_id, Order_id, count=1):
    Basket = MiningBasket.objects.filter(creator_id=current_user_id, status='draft').first() 
    if Basket == None:
        Basket = MiningBasket.objects.create(creator_id = User_id, status = 'draft')
    LinkBasketOrder.objects.get_or_create(basket_id=Basket.basket_id, order_id=Order_id, square=777)
    
def DelBasketController(request, id):
    if id!=None:
        cursor.execute('UPDATE mining_basket SET status = %s WHERE basket_id = %s', ("deleted", id,))
    conn.commit()
    return redirect(OrdersController)


def OrderAddController(request, id):
    order = getOrderById(id)
    if order == None:
        return redirect(OrdersController)
    addOrderToCurBasket(current_user_id, id)
    return redirect(OrdersController)
    
def BasketController(request, id):
    
    
    Basket = getDraftBasketByIdandUser(id, current_user_id)
    if Basket == None:
        return redirect(OrdersController)

    BasketOrders = getlinkBasketOrders(id)
    orders = []
    

    for BasketOrder in BasketOrders:
        order = getOrderById(BasketOrder.order_id)
        if order != None:
            orders.append({
                'image' : order.url,
                'name' : order.name,
                'dscr' : order.description,
                'price' : order.price
            })

    return render(request, 'basket.html', {'data' : {
        'id' : id,
        'orders':orders  
    }})

def OrdersController(request):

    Basket_count = 0
    cur_basket_id = -1

    Basket = MiningBasket.objects.filter(creator_id=current_user_id, status='draft').first()  

    if Basket!= None:
        Orders_in_current_busket = getlinkBasketOrders(Basket.basket_id)
        Basket_count = len(Orders_in_current_busket)
        cur_basket_id = Basket.basket_id

    search = ''
    if 'search_mining_order' in request.GET:
        search = request.GET['search_mining_order']

    orders_list_main = [] 

    Orders_found_by_search = MiningOrder.objects.filter(name__icontains=search)

    for order in Orders_found_by_search:
        isAdded = False
        if Basket!= None:
            for addedOrder in Orders_in_current_busket:
                if addedOrder.order_id == order.order_id:
                    isAdded = True
                    # Basket_count += 1
                    break
        orders_list_main.append({
                    'order_data': order,
                    'isAdded': isAdded
                })
    return render(request, 'orders.html', {'data' : {
        'orders': orders_list_main,
        'BasketCount' : Basket_count,
        'Basket_id' : cur_basket_id
        
    }})

def SingleOrderController(request, id):

    Order = getOrderById(id)    

    if Order == None:
        return redirect(OrdersController)

    return render(request, 'order.html', {'data':{
        'order' : Order
    }})

