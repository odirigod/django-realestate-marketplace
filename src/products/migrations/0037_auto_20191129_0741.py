# Generated by Django 2.2.1 on 2019-11-29 06:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0036_auto_20190716_1403'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productimage',
            options={'ordering': ['id']},
        ),
        migrations.AddField(
            model_name='productimage',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2019, 11, 29, 6, 41, 28, 564636, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productimage',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='bathroom',
            field=models.IntegerField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6+')], null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='bedroom',
            field=models.IntegerField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6+')], null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='property-for-sale-for-rent', max_length=200, unique=True),
        ),
    ]
