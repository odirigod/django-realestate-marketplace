# import datetime
# from datetime import datetime, timedelta
# from django.utils import timezone
# from decimal import Decimal
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.urls import reverse
# from django.core.signals import request_finished
# from django.dispatch import receiver

from django.db import models
# from django.db.models import Sum
from django.db.models.signals import pre_save, post_save, post_delete
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from markdown_deux import markdown

from dashboard.models import Profile





class PropertiesQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def available(self):
        return self.filter(available=True)



class ProductManager(models.Manager):
    
    def get_queryset(self):
        return PropertiesQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):
        return self.get_queryset()

    def get_products(self, *args, **kwargs):
        return self.get_queryset().active().available()

    def get_related(self, instance):
        qs = self.get_products().filter(category=instance.category).filter(property_type=instance.property_type).exclude(id=instance.id).order_by("?")#.distinct()
        return qs

    def get_featured(self):
        qs = self.get_products().filter(featured=True).order_by("?")
        return qs


STATE = (
  ('Abia', 'Abia'),
  ('Abuja', 'Abuja'),
  ('Adamawa', 'Adamawa'),
  ('Anambra', 'Anambra'),
  ('Akwa', 'Akwa Ibom'),
  ('Bauchi', 'Bauchi'),
  ('Bayelsa', 'Bayelsa'),
  ('Benue', 'Benue'),
  ('Borno', 'Borno'),
  ('Cross River', 'Cross River'),
  ('Delta', 'Delta'),
  ('Ebonyi', 'Ebonyi'),
  ('Edo', 'Edo'),
  ('Ekiti', 'Ekiti'),
  ('Enugu', 'Enugu'),
  ('Gombe', 'Gombe'),
  ('Imo', 'Imo'),
  ('Jigawa', 'Jigawa'),
  ('Kaduna', 'Kaduna'),
  ('Kano', 'Kano'),
  ('Katsina', 'Katsina'),
  ('Kebbi', 'Kebbi'),
  ('Kogi', 'Kogi'),
  ('Kwara', 'Kwara'),
  ('Lagos', 'Lagos'),
  ('Nasarawa', 'Nasarawa'),
  ('Niger', 'Niger'),
  ('Ogun', 'Ogun'),
  ('Ondo', 'Ondo'),
  ('Osun', 'Osun'),
  ('Oyo', 'Oyo'),
  ('Plateau', 'Plateau'),
  ('Rivers', 'Rivers'),
  ('Sokoto', 'Sokoto'),
  ('Taraba', 'Taraba'),
  ('Yobe', 'Yobe'),
  ('Zamfara', 'Zamfara'),
)

CATEGORIES = (
  ('For Sale', 'For Sale'),
  ('For Rent', 'For Rent'),
  ('For ShortLet', 'For ShortLet'),
)

PROPERTY_TYPE = (
    # ('Apartment', 'Apartment/Flat'),
    # ('Bungalow', 'Bungalow'),
    # ('Duplex', 'Duplex'),
    # ('Self Contain', 'Self Contain'),
    # ('Office Space', 'Office Space'),
    # ('Commercial', 'Commercial/Office'),
    # ('Filling Station', 'Filling Station'),
    ('Residential', 'Residential'),
    ('Commercial', 'Commercial'),
    ('Land', 'Land'),
)

NUMBER_LIST = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6+'),
    # (7, '7'),
    # (8, '8'),
    # (9, '9'),
    # (10, '10+'),
)



class Product(models.Model):
    pid = models.CharField(max_length=120, blank=True, null=True, unique=True, editable=False)
    realtor = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=200, unique=True, default="property-for-sale-for-rent")
    category = models.CharField(max_length=120, choices=CATEGORIES)
    property_type = models.CharField(max_length=120, choices=PROPERTY_TYPE)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    address = models.CharField(max_length=200)
    country = models.CharField(max_length=50, blank=True, null=True, default='Nigeria', editable=False)
    state = models.CharField(max_length=120, null=False, blank=False, choices=STATE)
    city = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(blank=False, null=False)
    area = models.IntegerField(null=True, blank=True)
    bedroom = models.IntegerField(null=True, blank=True, choices=NUMBER_LIST)
    bathroom = models.IntegerField(null=True, blank=True, choices=NUMBER_LIST)
    parking = models.IntegerField(null=True, blank=True)
    patio = models.IntegerField(null=True, blank=True)
    available = models.BooleanField(default=True)
    boosted = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    objects = ProductManager()

    class Meta:
        ordering = ["-boosted", "-timestamp", "-title"]

    def __str__(self):
        return "%s" %(self.pid)

    def get_absolute_url(self):
        return reverse("products:product_redirect", kwargs={"pid": self.pid})

    def get_image_url(self):
        img = self.productimage_set.first()
        if img:
          try:
            img = img.media.url
          except:
            img = None
            # return img.media.url
        return img #None

    def get_images(self):
        img = self.productimage_set.all()[:6]
        return img


    def get_markdown(self):
        description = self.description
        markdown_text = markdown(description)
        return mark_safe(markdown_text)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.pid = 10000 + self.id
        super().save(*args, **kwargs)



# def create_slug(instance, new_slug=None):
#   slug = slugify(instance.title)
#   if new_slug is not None:
#     slug = new_slug
#   qs = Product.objects.filter(slug=slug)
#   exists = qs.exists()
#   if exists:
#     new_slug = "%s-%s" %(slug, qs.first().pid)
#     return create_slug(instance, new_slug=new_slug)
#   return slug



# def product_pre_save_receiver(sender, instance, *args, **kwargs):
#   if not instance.slug:
#     instance.slug = create_slug(instance)


def product_pre_save_receiver(sender, instance, *args, **kwargs):
  new_slug = slugify(instance.title)
  instance.slug = "%s-%s" %(new_slug, instance.pid)

pre_save.connect(product_pre_save_receiver, sender=Product)






def media_location(instance, filename):
    title = instance.product.title
    slug = slugify(title)
    filebase = filename.split(".")[0]
    # new_filename = "%s.%s" %(instance.properties.pid, file_extension)
    # return "properties/%s/%s" %(instance.properties.realtor, new_filename)
    return "products/%s/%s/%s.png" %(instance.product.realtor.user.email, instance.product.pid, filebase)


def image_validation(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 2.0
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError("Image too large, Maximum size allowed is %sMB" %(megabyte_limit))


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    media = models.ImageField(
        width_field = "width",
        height_field = "height",
        null = True,
        # blank = True,
        upload_to = media_location,
        validators=[image_validation]
      )
    width = models.CharField(max_length=20, null=True, blank=True)
    height = models.CharField(max_length=20, null=True, blank=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return "%s" %(self.product.title)

    def get_image_update_url(self):
        return reverse("dashboard:product_image_update", kwargs={"slug": self.product.pid})





class Wishlist(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

  def __str__(self):
    return "%s" %(self.product)

  class Meta:
    verbose_name = "Wishlist"
    verbose_name_plural = "Wishlist"
    ordering = ["-timestamp"]




