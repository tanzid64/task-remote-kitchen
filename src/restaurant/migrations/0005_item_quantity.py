# Generated by Django 5.1.1 on 2024-09-06 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_alter_item_item_name_alter_menu_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='quantity',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
