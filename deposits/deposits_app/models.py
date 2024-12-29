from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, BaseUserManager
from django.contrib.auth.models import Group, Permission

# class AuthUser(models.Model):
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.BooleanField()
#     username = models.CharField(unique=True, max_length=150)
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     email = models.CharField(max_length=254)
#     is_staff = models.BooleanField()
#     is_active = models.BooleanField()
#     date_joined = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         managed = False
#         db_table = 'auth_user'

class NewUserManager(UserManager):
    def create_user(self,email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        
        email = self.normalize_email(email) 
        user = self.model(email=email, username = username, **extra_fields) 
        user.set_password(password)
        user.save(using=self.db)
        return user




class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(("email адрес"), max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True, verbose_name="Имя пользователя")
    password = models.CharField(max_length=100, verbose_name="Пароль")    
    is_staff = models.BooleanField(default=False, verbose_name="Является ли пользователь менеджером?")
    is_superuser = models.BooleanField(default=False, verbose_name="Является ли пользователь админом?")
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')

    USERNAME_FIELD = 'username'

    objects =  NewUserManager()

    groups = models.ManyToManyField(
        Group,
        related_name = 'CustomUserGroups',
        blank = True,
        verbose_name = 'Группы',
        through='CustomUserGroup'
    )

    user_permissions = models.ManyToManyField(
        Permission, 
        related_name = 'CustomUserPermissions',
        blank = True,
        verbose_name = 'Разрешения',
        through='CustomUserPermission'
    )

    class Meta:
        managed = False
        db_table = 'auth_user'                      

class CustomUserGroup(models.Model):
    custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        db_table = 'custom_user_groups'

class CustomUserPermission(models.Model):
    custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        db_table = 'custom_user_permissions'


class MiningOrder(models.Model):
    mining_order_id = models.AutoField(primary_key=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    formation_date = models.DateTimeField(blank=True, null=True)
    company_name = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    mining_start_date = models.DateTimeField(blank=True, null=True)
    status = models.TextField()
    creator = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, null=True, related_name='UserMiningOrders')
    moderator = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, null=True, related_name='ModeratorMiningOrders')
    order_cost = models.IntegerField(blank=True, null=True)
    moderation_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mining_order'


class MiningService(models.Model):
    mining_service_id = models.AutoField(primary_key=True)
    name = models.TextField(unique=True, blank=True, null=True)
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




class Attributes(models.Model):
    id = models.AutoField(primary_key=True)
    attribute_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'attributes'


class AttributesServicesMm(models.Model):
    id = models.AutoField(primary_key=True)
    attribute = models.ForeignKey(Attributes, on_delete=models.DO_NOTHING, related_name='attribute_services')
    service = models.ForeignKey(MiningService, on_delete=models.DO_NOTHING, related_name='service_attributes')
    value = models.TextField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'attributes_services_mm'
        unique_together = (('service_id', 'attribute_id'),)