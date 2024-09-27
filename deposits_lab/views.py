from django.shortcuts import render
from datetime import date


baskets_list = [
    {
        'id': 1,
        'ItemIds':[2, 4, 1],
        'Organisation_name': 'Норникель' ,
        'Mining_place': 'Кольский полуостров' ,
        'Start_date': '30.08.25' 

    },
    {
        'id': 2,
        'ItemIds':[],
        'Organisation_name': 'Русал' ,
        'Mining_place': 'Ухта' ,
        'Start_date': '26.05.25'
    },
    {
        'id': 3,
        'ItemIds':[2, 6, 7, 1],
        'Organisation_name': 'Оренбургские минералы' ,
        'Mining_place': 'Оренбургская область' ,
        'Start_date': '01.12.24'
    }
]

orders_list = [
    {'image': 'http://localhost:9000/images/pic1.png',
    'name': 'Геологическая разведка',
    'dscr': 'Поиск и оценка месторождений полезных ископаемых',
    'price': '50 000 рублей',
    'long_dscr': 'Услуги по геологической разведке, поиску и оценке месторождений полезных ископаемых: россыпного и рудного золота, строительного камня, песчано-гравийной смеси, песка, глины. Наши клиенты — организации, которые занимаются разработкой горных месторождений, осуществляют добычу и перерабатывают полезные ископаемые, выполняют прочие работы в отношении минерально-сырьевой базы. Многолетнее присутствие на рынке и богатый опыт позволяет нам оперативно проводить геологоразведку недр и предоставлять клиентам требуемые геологические данные.' ,
    'id': 1
    },
    {'image': 'http://localhost:9000/images/pic2.png',
    'name': 'Проектирование горных работ',
    'dscr': 'Услуги по проектированию горных работ',
    'price': '100 000 рублей',
    'long_dscr': 'Услуги по проектированию горных работ: разработка, подготовка, сопровождение согласования и утверждение проектной документации для предприятий по добыче полезных ископаемых. Горный проект включает подготовительные, горно-строительные, вскрышные, добычные и прочие работы, которые проводятся в процессе освоения новых месторождений. Нашими клиентами являются предприятия, которые занимаются разработкой и добычей рудных и нерудных полезных ископаемых из недр, предоставленных в пользование.' ,
    'id': 2
    },
    {'image': 'http://localhost:9000/images/pic3.png',
    'name': 'Геологические работы',
    'dscr': 'Подсчет запасов и выполнение технико-экономического расчета месторождения',
    'price': '30 000 рублей',
    'long_dscr': 'Геологические работы на участке, в том числе инженерно-геологическая съемка. Мы оказываем весь комплекс услуг под ключ — начиная с подсчета запасов и выполнения технико-экономического расчета месторождения и заканчивая подготовкой отчетной документации и оцифровкой полученной информации. У нас работают квалифицированные инженеры-геологи с большим опытом, способные оперативно и эффективно решать задачи любой сложности, обеспечивая максимально точные результаты.' ,
    'id': 3
    },
    {'image':  'http://localhost:9000/images/pic4.png',  
    'name': 'Маркшейдерские работы',
    'dscr': 'Маркшейдерское обеспечение горных работ',
    'price': '60 000 рублей',
    'long_dscr': 'Обеспечение на карьерах, месторождениях полезных ископаемых, строительных площадках. Мы работаем с государственными организациями и частными предприятиями в соответствии с требованиями действующего законодательства. Располагаем современным оборудованием, имеем в своем штате опытных квалифицированных инженеров-маркшейдеров, способных быстро, качественно и точно выполнять работы любого уровня сложности' ,
    'id': 4
    },
    {'image': 'http://localhost:9000/images/pic5.png', 
    'name': 'Сканирование и аэрофотосъемка',
    'dscr': 'Точные данные о рельефе местности',
    'price': '10 000 рублей',
    'long_dscr': 'Топографическая аэрофотосъемка представляет собой один из наиболее информативных методов сбора точных пространственных данных о рельефе местности. С ее помощью можно быстро и с минимальными финансовыми затратами получить изображения территории в высоком разрешении, а также полный комплекс необходимой информации.' ,
    'id': 5
    },
    {'image': 'http://localhost:9000/images/pic6.png', 
    'name': 'Геодезические работы',
    'dscr': 'Комплекс инженерно-геодезических работ',
    'price': '80 000 рублей',
    'long_dscr': 'Полный комплекс инженерно-геодезических работ на объектах различного назначения. Наши услуги направлены на получение полных и достоверных данных об условиях площадки строительства. Осуществляем производство геодезических работ по всей территории России.' ,
    'id': 6
    },
    {'image': 'http://localhost:9000/images/pic7.png', 
    'name': 'Аудит горнодобывающих предприятий',
    'dscr': 'Полная проверка хозяйственной деятельности',
    'price': '30 000 рублей',
    'long_dscr': 'Аудит горнодобывающих предприятий/карьеров. Мы проведем полную проверку хозяйственной деятельности, что даст возможность выявить недостатки в организации и осуществлении технических горных работ, связанных с разработкой месторождений. В штате только опытные специалисты, которые быстро и правильно проведут все исследования и дадут рекомендации по повышению эффективности добычи полезных ископаемых.' ,
    'id': 7
    }
]

def BasketController(request, id):

    orders_list_basket = []

    for basket in baskets_list:
        if basket['id'] == id:
            for i in basket['ItemIds']:
                for order in orders_list:
                    if order['id'] == i:
                        orders_list_basket.append(order)

    return render(request, 'basket.html', {'data' : {
        'id': id,
        'baskets' : baskets_list,
        'orders': orders_list_basket
    }})

def OrdersController(request):

    basket_id = 3

    BasketCount = 0
    for basket in baskets_list:
        if basket['id'] == basket_id:
            BasketCount =  len(basket['ItemIds'])

    search = ''
    if 'search_mining_order' in request.GET:
        search = request.GET['search_mining_order']

    orders_list_main = []

    for order in orders_list:
        if search.lower() in order['name'].lower():
            orders_list_main.append(order)

    print (BasketCount)
    return render(request, 'orders.html', {'data' : {
        'orders': orders_list_main,
        'BasketCount' : BasketCount,
        'Basket_id' : basket_id
    }})

def SingleOrderController(request, id):
    return render(request, 'order.html', {'data' : {
        'order' : orders_list[id-1],
        'id': id
    }})

