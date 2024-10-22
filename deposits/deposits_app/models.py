from django.db import models

class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'auth_user'


class MiningOrder(models.Model):
    mining_order_id = models.AutoField(primary_key=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    formation_date = models.DateTimeField(blank=True, null=True)
    company_name = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    mining_start_date = models.DateTimeField(blank=True, null=True)
    status = models.TextField()
    creator = models.ForeignKey(AuthUser, on_delete=models.DO_NOTHING, null=True, related_name='UserMiningOrders')
    moderator = models.ForeignKey(AuthUser, on_delete=models.DO_NOTHING, null=True, related_name='ModeratorMiningOrders')
    order_cost = models.IntegerField(blank=True, null=True)
    moderation_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mining_order'


class MiningService(models.Model):
    mining_service_id = models.AutoField(primary_key=True)
    name = models.TextField(unique=True)
    description = models.TextField(unique=True, blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    url = models.TextField(unique=True, blank=True, null=True)
    long_description = models.TextField(unique=True, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mining_service'

class LinkServicesOrders(models.Model):
    id = models.AutoField(primary_key=True)
    mining_order = models.ForeignKey(MiningOrder, on_delete=models.DO_NOTHING, related_name='linked_mining_orders')
    mining_service = models.ForeignKey(MiningService, on_delete=models.DO_NOTHING, related_name='linked_mining_services')
    square = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'link_services_orders'
        unique_together = (('mining_order_id', 'mining_service_id'),)
