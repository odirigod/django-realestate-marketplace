# Generated by Django 2.2.1 on 2019-06-13 10:32

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20190610_1921'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='media',
            field=models.ImageField(blank=True, default=1, height_field='height', upload_to=products.models.media_location, validators=[products.models.image_validation], width_field='width'),
            preserve_default=False,
        ),
    ]
