from django.db import models

class LinkServiceOrder(models.Model):
    mining_order_id = models.IntegerField()
    mining_service_id = models.IntegerField()
    square = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'link_services_orders'
        unique_together = (('mining_order_id', 'mining_service_id'),)

class MiningOrder(models.Model):
    mining_order_id = models.AutoField(primary_key=True)
    creation_date = models.DateTimeField(blank=True, null=True)
    formation_date = models.DateTimeField(blank=True, null=True)
    ending_date = models.DateTimeField(blank=True, null=True)
    company_name = models.TextField()
    location = models.TextField()
    mining_start_date = models.DateTimeField()
    status = models.TextField()
    creator_id = models.IntegerField(blank=True, null=True)
    moderator_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mining_order'


class MiningService(models.Model):
    mining_service_id = models.AutoField(primary_key=True)
    name = models.TextField(unique=True)
    description = models.TextField(unique=True)
    status = models.TextField()
    url = models.TextField(unique=True)
    long_description = models.TextField(unique=True)
    price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mining_service'
