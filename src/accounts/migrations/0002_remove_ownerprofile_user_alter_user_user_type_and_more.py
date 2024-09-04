# Generated by Django 5.1.1 on 2024-09-04 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('restaurant', '0002_alter_restaurant_employees_alter_restaurant_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ownerprofile',
            name='user',
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('CUSTOMER', 'Customer'), ('OWNER', 'Owner'), ('EMPLOYEE', 'Employee')], default='CUSTOMER', max_length=10, verbose_name='User Type'),
        ),
        migrations.DeleteModel(
            name='EmployeeProfile',
        ),
        migrations.DeleteModel(
            name='OwnerProfile',
        ),
    ]
