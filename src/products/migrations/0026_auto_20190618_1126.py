# Generated by Django 2.2.1 on 2019-06-18 10:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0025_auto_20190618_1124'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='height',
        ),
        migrations.RemoveField(
            model_name='productimage',
            name='media',
        ),
        migrations.RemoveField(
            model_name='productimage',
            name='width',
        ),
    ]
