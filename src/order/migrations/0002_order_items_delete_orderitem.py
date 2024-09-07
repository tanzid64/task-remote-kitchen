# Generated by Django 5.1.1 on 2024-09-06 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
        ('restaurant', '0004_alter_item_item_name_alter_menu_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(related_name='orders', to='restaurant.item'),
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
