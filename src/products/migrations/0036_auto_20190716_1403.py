# Generated by Django 2.2.1 on 2019-07-16 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0035_auto_20190716_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='property-for-sale-or-for-rent', max_length=120),
        ),
    ]
