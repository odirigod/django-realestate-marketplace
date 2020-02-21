# Generated by Django 2.2.1 on 2019-06-13 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_auto_20190613_1132'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rid', models.CharField(blank=True, editable=False, max_length=30, null=True, unique=True)),
                ('title', models.CharField(max_length=120)),
                ('category', models.CharField(choices=[('For Sale', 'For Sale'), ('For Rent', 'For Rent'), ('For ShortLet', 'For ShortLet')], max_length=120)),
                ('property_type', models.CharField(choices=[('Apartment', 'Apartment/Flat'), ('Bungalow', 'Bungalow'), ('Duplex', 'Duplex'), ('Self Contain', 'Self Contain'), ('Commercial', 'Commercial/Office'), ('Land', 'Land')], max_length=120)),
                ('minimum_price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('maximum_price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('address', models.CharField(max_length=200)),
                ('country', models.CharField(blank=True, default='Nigeria', editable=False, max_length=50, null=True)),
                ('state', models.CharField(choices=[('Abia', 'Abia'), ('Abuja', 'Abuja'), ('Adamawa', 'Adamawa'), ('Anambra', 'Anambra'), ('Akwa', 'Akwa Ibom'), ('Bauchi', 'Bauchi'), ('Bayelsa', 'Bayelsa'), ('Benue', 'Benue'), ('Borno', 'Borno'), ('Cross River', 'Cross River'), ('Delta', 'Delta'), ('Ebonyi', 'Ebonyi'), ('Edo', 'Edo'), ('Ekiti', 'Ekiti'), ('Enugu', 'Enugu'), ('Gombe', 'Gombe'), ('Imo', 'Imo'), ('Jigawa', 'Jigawa'), ('Kaduna', 'Kaduna'), ('Kano', 'Kano'), ('Katsina', 'Katsina'), ('Kebbi', 'Kebbi'), ('Kogi', 'Kogi'), ('Kwara', 'Kwara'), ('Lagos', 'Lagos'), ('Nasarawa', 'Nasarawa'), ('Niger', 'Niger'), ('Ogun', 'Ogun'), ('Ondo', 'Ondo'), ('Osun', 'Osun'), ('Oyo', 'Oyo'), ('Plateau', 'Plateau'), ('Rivers', 'Rivers'), ('Sokoto', 'Sokoto'), ('Taraba', 'Taraba'), ('Yobe', 'Yobe'), ('Zamfara', 'Zamfara')], max_length=120)),
                ('city', models.CharField(max_length=200)),
                ('comment', models.TextField()),
                ('active', models.BooleanField(default=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Profile')),
            ],
            options={
                'ordering': ['-timestamp', '-updated', '-title'],
            },
        ),
    ]
