from django.contrib import admin
from .models import  LinkServiceOrder, MiningService, MiningOrder

admin.site.register(LinkServiceOrder)
admin.site.register(MiningService)
admin.site.register(MiningOrder)

