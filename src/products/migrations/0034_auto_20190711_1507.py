# Generated by Django 2.2.1 on 2019-07-11 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0033_auto_20190625_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='property_type',
            field=models.CharField(choices=[('Residential', 'Residential'), ('Commercial', 'Commercial'), ('Land', 'Land')], max_length=120),
        ),
    ]
