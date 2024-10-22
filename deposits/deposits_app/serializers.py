from deposits_app.models import LinkServicesOrders
from deposits_app.models import MiningOrder
from deposits_app.models import MiningService
from rest_framework import serializers
from deposits_app.models import AuthUser

class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = '__all__'

class MiningServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiningService
        fields = '__all__'

class MiningOrdermmfieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiningOrder
        fields = ["company_name", "location", "mining_start_date"]

class MiningServiceOrderSerializer(serializers.ModelSerializer):
    Mservice = MiningServiceSerializer(source = 'mining_service', read_only=True)

    class Meta:
        model = LinkServicesOrders
        fields = ["id", "Mservice", "square"]

class MiningOrdersSerialiser(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()
    moderator = serializers.StringRelatedField()

    class Meta:
        model = MiningOrder
        fields = ["mining_order_id", "status", "creation_date", "formation_date", "moderation_date", "company_name", "location", 
                  "mining_start_date", "creator", "moderator"]

class SingleMiningOrderSerializer(serializers.ModelSerializer):
    mining_services_in_order = MiningServiceOrderSerializer(source = 'linked_mining_orders',  many = True, read_only = True)
    creator = serializers.StringRelatedField()
    moderator = serializers.StringRelatedField()

    class Meta:
        model = MiningOrder
        fields = ["mining_order_id", "status", "creation_date", "formation_date", "moderation_date", "company_name", "location", 
                  "mining_start_date", "mining_services_in_order", "creator", "moderator"]

