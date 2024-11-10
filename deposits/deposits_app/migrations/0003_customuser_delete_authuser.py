# Generated by Django 4.2.4 on 2024-11-10 14:48

import deposits_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('deposits_app', '0002_authuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email адрес')),
                ('username', models.CharField(max_length=50, verbose_name='Имя пользователя')),
                ('password', models.CharField(max_length=50, verbose_name='Пароль')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Является ли пользователь менеджером?')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Является ли пользователь админом?')),
                ('groups', models.ManyToManyField(blank=True, related_name='CustomUserGroups', to='auth.group', verbose_name='Группы')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='CustomUserPermissions', to='auth.permission', verbose_name='Разрешения')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', deposits_app.models.NewUserManager()),
            ],
        ),
        migrations.DeleteModel(
            name='AuthUser',
        ),
    ]
