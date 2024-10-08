# Generated by Django 5.1.1 on 2024-09-06 16:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0003_alter_restaurant_owner'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_name',
            field=models.CharField(max_length=200, verbose_name='Item Name'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Menu Name'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='employees',
            field=models.ManyToManyField(blank=True, related_name='employees', to=settings.AUTH_USER_MODEL),
        ),
    ]
