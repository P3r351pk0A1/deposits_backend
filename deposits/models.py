from django.db import models

class LinkBasketOrder(models.Model):
    basket_id = models.IntegerField()
    order_id = models.IntegerField()
    square = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'link_basket_orders'
        unique_together = (('basket_id', 'order_id'),)

class MiningBasket(models.Model):
    basket_id = models.AutoField(primary_key=True)
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
        db_table = 'mining_basket'


class MiningOrder(models.Model):
    order_id = models.AutoField(primary_key=True)
    name = models.TextField(unique=True)
    description = models.TextField(unique=True)
    status = models.TextField()
    url = models.TextField(unique=True)
    long_description = models.TextField(unique=True)
    price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mining_orders'


class User(models.Model):
    login = models.TextField(primary_key=True)
    password = models.TextField()
    role = models.TextField()

    class Meta:
        managed = False
        db_table = 'users'
