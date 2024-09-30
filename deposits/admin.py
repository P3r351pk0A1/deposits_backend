from django.contrib import admin
from .models import  LinkBasketOrder, MiningBasket, MiningOrder, User

admin.site.register(LinkBasketOrder)
admin.site.register(MiningBasket)
admin.site.register(MiningOrder)
admin.site.register(User)
