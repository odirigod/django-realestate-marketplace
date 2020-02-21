from django.db import models
# # import datetime
# # from datetime import datetime, timedelta
# # from django.utils import timezone
# # from decimal import Decimal
# from django.conf import settings
# from django.contrib.auth.models import User
# from django.core.validators import RegexValidator
# from django.core.exceptions import ValidationError
# from django.urls import reverse
# # from django.core.signals import request_finished
# # from django.dispatch import receiver


# # from django.db.models import Sum
# from django.db.models.signals import pre_save, post_save, post_delete
# from django.utils.safestring import mark_safe
# from django.utils.text import slugify
# from markdown_deux import markdown

# from dashboard.models import Profile





# class ClientRequestQuerySet(models.query.QuerySet):
#     def active(self):
#         return self.filter(active=True)

#     # def available(self):
#     #     return self.filter(available=True)



# class ClientRequestManager(models.Manager):
    
#     def get_queryset(self):
#         return ClientRequestQuerySet(self.model, using=self._db)

#     def all(self, *args, **kwargs):
#         return self.get_queryset()

#     # def get_client_request(self, *args, **kwargs):
#     #     return self.get_queryset().active().available()

#     def get_related(self, instance):
#         qs = self.all().filter(category=instance.category).filter(property_type=instance.property_type).exclude(id=instance.id).order_by("?")#.distinct()
#         return qs

# STATE = (
#   ('Abia', 'Abia'),
#   ('Abuja', 'Abuja'),
#   ('Adamawa', 'Adamawa'),
#   ('Anambra', 'Anambra'),
#   ('Akwa', 'Akwa Ibom'),
#   ('Bauchi', 'Bauchi'),
#   ('Bayelsa', 'Bayelsa'),
#   ('Benue', 'Benue'),
#   ('Borno', 'Borno'),
#   ('Cross River', 'Cross River'),
#   ('Delta', 'Delta'),
#   ('Ebonyi', 'Ebonyi'),
#   ('Edo', 'Edo'),
#   ('Ekiti', 'Ekiti'),
#   ('Enugu', 'Enugu'),
#   ('Gombe', 'Gombe'),
#   ('Imo', 'Imo'),
#   ('Jigawa', 'Jigawa'),
#   ('Kaduna', 'Kaduna'),
#   ('Kano', 'Kano'),
#   ('Katsina', 'Katsina'),
#   ('Kebbi', 'Kebbi'),
#   ('Kogi', 'Kogi'),
#   ('Kwara', 'Kwara'),
#   ('Lagos', 'Lagos'),
#   ('Nasarawa', 'Nasarawa'),
#   ('Niger', 'Niger'),
#   ('Ogun', 'Ogun'),
#   ('Ondo', 'Ondo'),
#   ('Osun', 'Osun'),
#   ('Oyo', 'Oyo'),
#   ('Plateau', 'Plateau'),
#   ('Rivers', 'Rivers'),
#   ('Sokoto', 'Sokoto'),
#   ('Taraba', 'Taraba'),
#   ('Yobe', 'Yobe'),
#   ('Zamfara', 'Zamfara'),
# )

# CATEGORIES = (
#   ('For Sale', 'For Sale'),
#   ('For Rent', 'For Rent'),
#   ('For ShortLet', 'For ShortLet'),
# )

# PROPERTY_TYPE = (
#     ('Apartment', 'Apartment/Flat'),
#     ('Bungalow', 'Bungalow'),
#     ('Duplex', 'Duplex'),
#     ('Self Contain', 'Self Contain'),
#     # ('Office Space', 'Office Space'),
#     ('Commercial', 'Commercial/Office'),
#     ('Land', 'Land'),
# )

# NUMBER_LIST = (
#     (1, '1'),
#     (2, '2'),
#     (3, '3'),
#     (4, '4'),
#     (5, '5'),
#     (6, '6'),
#     (7, '7'),
#     (8, '8'),
#     (9, '9'),
#     (10, '10+'),
# )



# class ClientRequest(models.Model):
#     user = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     rid = models.CharField(max_length=30, blank=True, null=True, unique=True, editable=False)
#     title = models.CharField(max_length=120)
#     category = models.CharField(max_length=120, choices=CATEGORIES)
#     property_type = models.CharField(max_length=120, choices=PROPERTY_TYPE)
#     minimum_price = models.DecimalField(max_digits=20, decimal_places=2)
#     maximum_price = models.DecimalField(max_digits=20, decimal_places=2)
#     address = models.CharField(max_length=200)
#     country = models.CharField(max_length=50, blank=True, null=True, default='Nigeria', editable=False)
#     state = models.CharField(max_length=120, null=False, blank=False, choices=STATE)
#     city = models.CharField(max_length=200, null=False, blank=False)
#     description = models.TextField(blank=False, null=False)
#     # area = models.IntegerField(null=True, blank=True)
#     # bedroom = models.IntegerField(null=True, blank=True)
#     # bathroom = models.IntegerField(null=True, blank=True)
#     # parking = models.IntegerField(null=True, blank=True)
#     # available = models.BooleanField(default=True)
#     active = models.BooleanField(default=True)
#     updated = models.DateTimeField(auto_now_add=False, auto_now=True)
#     timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

#     objects = ClientRequestManager()

#     class Meta:
#         ordering = ["-timestamp", "-updated", "-title"]

#     def __str__(self):
#         return "%s" %(self.title)

#     def get_absolute_url(self):
#         return reverse("dashboard:client_request", kwargs={"rid": self.rid})

#     def get_markdown(self):
#         description = self.description
#         markdown_text = markdown(description)
#         return mark_safe(markdown_text)


#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         self.rid = 30000 + self.id
#         super().save(*args, **kwargs)


