from deposits_app.models import LinkServicesOrders
from deposits_app.models import MiningOrder
from deposits_app.models import MiningService
from rest_framework import serializers
# from deposits_app.models import AuthUser
from deposits_app.models import CustomUser
from collections import OrderedDict


# class AuthUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AuthUser
#         fields = '__all__'

#         def get_fields(self):
#             new_fields = OrderedDict()
#             for name, field in super().get_fields().items():
#                 field.required = False
#                 new_fields[name] = field
#             return new_fields 

class MiningServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiningService
        fields = '__all__'

        def get_fields(self):
            new_fields = OrderedDict()
            for name, field in super().get_fields().items():
                field.required = False
                new_fields[name] = field
            return new_fields 

#сериалайзер ради вложенности
class MiningServiceSerializerInserted(serializers.ModelSerializer):
    class Meta:
        model = MiningService
        fields = ["name", "status", "url", "price"]
        
        def get_fields(self):
            new_fields = OrderedDict()
            for name, field in super().get_fields().items():
                field.required = False
                new_fields[name] = field
            return new_fields 

class MiningOrdermmfieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiningOrder
        fields = ["company_name", "location", "mining_start_date"]

        def get_fields(self):
            new_fields = OrderedDict()
            for name, field in super().get_fields().items():
                field.required = False
                new_fields[name] = field
            return new_fields 
        
class MiningServiceOrderSerializer(serializers.ModelSerializer):
    Mservice = MiningServiceSerializer(source = 'mining_service', read_only=True)

    class Meta:
        model = LinkServicesOrders
        fields = ["id", "Mservice", "square"]

        def get_fields(self):
            new_fields = OrderedDict()
            for name, field in super().get_fields().items():
                field.required = False
                new_fields[name] = field
            return new_fields 
        
class MiningOrdersSerialiser(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()
    moderator = serializers.StringRelatedField()

    class Meta:
        model = MiningOrder
        fields = ["mining_order_id", "status", "creation_date", "formation_date", "moderation_date", "company_name", "location", 
                  "mining_start_date", "creator", "moderator", "order_cost"]

        def get_fields(self):
            new_fields = OrderedDict()
            for name, field in super().get_fields().items():
                field.required = False
                new_fields[name] = field
            return new_fields 
        
#сериалайзер ради вложенности
class MiningServiceOrderSerializerInserted(serializers.ModelSerializer):
    Mservice = MiningServiceSerializerInserted(source = 'mining_service', read_only=True)

    class Meta:
        model = LinkServicesOrders
        fields = ["Mservice", "square"]

        def get_fields(self):
            new_fields = OrderedDict()
            for name, field in super().get_fields().items():
                field.required = False
                new_fields[name] = field
            return new_fields 
        
class SingleMiningOrderSerializer(serializers.ModelSerializer):
    mining_services_in_order = MiningServiceOrderSerializerInserted(source = 'linked_mining_orders',  many = True, read_only = True)
    creator = serializers.StringRelatedField()
    moderator = serializers.StringRelatedField()

    class Meta:
        model = MiningOrder
        fields = ["mining_order_id", "status", "creation_date", "formation_date", "moderation_date", "company_name", "location", 
                  "mining_start_date", "order_cost", "mining_services_in_order", "creator", "moderator"]

        def get_fields(self):
            new_fields = OrderedDict()
            for name, field in super().get_fields().items():
                field.required = False
                new_fields[name] = field
            return new_fields 
        
class UserSerializer(serializers.ModelSerializer):
    is_staff = serializers.BooleanField(default=False, required=False)
    is_superuser = serializers.BooleanField(default=False, required=False)
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'is_staff', 'is_superuser', 'username']

        def get_fields(self):
            new_fields = OrderedDict()
            for name, field in super().get_fields().items():
                field.required = False
                new_fields[name] = field
            return new_fields 
