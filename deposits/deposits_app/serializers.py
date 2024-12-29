from deposits_app.models import LinkServicesOrders
from deposits_app.models import MiningOrder
from deposits_app.models import MiningService
from deposits_app.models import AttributesServicesMm
from deposits_app.models import Attributes
from rest_framework import serializers
# from deposits_app.models import AuthUser
from deposits_app.models import CustomUser
from collections import OrderedDict

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
        
class LinkServiceOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkServicesOrders
        fields = '__all__'

        def get_fields(self):
            new_fields = OrderedDict()
            for name, field in super().get_fields().items():
                field.required = False
                new_fields[name] = field
            return new_fields

class MServicesListSerializer(serializers.Serializer):
    name = serializers.CharField()

class MiningServiceResponseSerializer(serializers.Serializer):
    mining_service_id = serializers.IntegerField()
    name = serializers.CharField()


class ActiveMOrderSerializer(serializers.Serializer):
    MiningServicesInUsersDraft = serializers.IntegerField()
    UsersDraftId = serializers.IntegerField()
    
class MiningServicesListResponseSerializer(serializers.Serializer):
    services = MiningServiceSerializer(many = True)
    active_m_order = ActiveMOrderSerializer()
    MServicesInCurOrder = LinkServiceOrderSerializer(many = True)

class ModifyMiningOrderSerializer(serializers.Serializer):
    mining_order_id = serializers.IntegerField()
    company_name = serializers.CharField()
    mining_start_date = serializers.DateTimeField()
    location = serializers.CharField()



#сериалайзер ради вложенности
class MiningServiceSerializerInserted(serializers.ModelSerializer):
    class Meta:
        model = MiningService
        fields = ["mining_service_id", "name", "status", "url", "price"]
        
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
        
class MiningOrdersListResponseSerializer(serializers.Serializer):
    mining_orders = MiningOrdersSerialiser(many = True)

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
        fields = ['email', 'password', 'is_staff', 'is_superuser', 'username', 'first_name', 'last_name']

        def get_fields(self):
            new_fields = OrderedDict()
            for name, field in super().get_fields().items():
                field.required = False
                new_fields[name] = field
            return new_fields 

class AttributesServicesMmSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(source='attribute.attribute_name', read_only=True)
    # service_id = serializers.IntegerField(read_only=True)
    value = serializers.CharField(read_only=True)

    class Meta:
        model = AttributesServicesMm
        fields = ['attribute_name',  'value']

        def get_fields(self):
            new_fields = OrderedDict()
            for name, field in super().get_fields().items():
                field.required = False
                new_fields[name] = field
            return new_fields
        
class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attributes
        fields = ['id', 'attribute_name']

        def get_fields(self):
            new_fields = OrderedDict()
            for name, field in super().get_fields().items():
                field.required = False
                new_fields[name] = field
            return new_fields
        
class AttributeRequestSerializer(serializers.Serializer):
    attribute_name = serializers.CharField()
    attribute_value = serializers.CharField()
    service_id = serializers.IntegerField()

class AttributeResponseSerializer(serializers.Serializer):
    attribute_name = serializers.CharField()

class MiningServiceResponseSerializer(serializers.Serializer):
    mining_service = MiningServiceSerializer()
    service_attributes = AttributesServicesMmSerializer(many = True)


