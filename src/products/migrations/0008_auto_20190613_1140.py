# Generated by Django 2.2.1 on 2019-06-13 10:40

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20190613_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='media',
            field=models.ImageField(height_field='height', null=True, upload_to=products.models.media_location, validators=[products.models.image_validation], width_field='width'),
        ),
    ]
