import datetime
from datetime import datetime, timedelta
from django.utils import timezone
from decimal import Decimal
from django.conf import settings
from django.contrib.auth.models import User
from django.core.signals import request_finished
from django.core.validators import RegexValidator
from django.dispatch import receiver
from django.urls import reverse

from django.db import models
from django.db.models import Sum
from django.db.models.signals import pre_save, post_save, post_delete
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from markdown_deux import markdown

# from products.models import Product


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


WHO_YOU_ARE = (
	('Individual', 'Individual'),
	('Agent', 'Property Agent'),
	('Owner', 'Property Owner'),
  ('Developer', 'Property Developer'),
)



def image_upload_to_profile(instance, filename):
    username = instance.user.username
    # slug = slugify(title)
    return "profiles/%s/%s" % (username, filename)
    # file_extension = filename.split(".")[1]
    # new_filename = "%s.%s" % (instance.id, file_extension)
    # return "profiles/%s/%s" % (slug, new_filename)

def image_validation(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 2.0
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError("Image too large, Maximum size allowed is %sMB" %(megabyte_limit))

        
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    ref = models.CharField(max_length=30, blank=True, null=True, unique=True, editable=False)
    image = models.ImageField(upload_to=image_upload_to_profile,
            null=True,
            # blank=True,
            width_field="width_field",
            height_field="height_field",
            validators=[image_validation])
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    phone = models.CharField(max_length=11, blank=False, null=False, unique=True, validators=[RegexValidator(regex='^[0-9]{11}$', message='Please enter a valid phone number', code='invalid number')])
    whatsapp = models.CharField(max_length=11, blank=False, null=False, unique=True, validators=[RegexValidator(regex='^[0-9]{11}$', message='Please enter a valid phone number', code='invalid number')])
    who_are_you = models.CharField(max_length=120, choices=WHO_YOU_ARE)
    company = models.CharField(max_length=200, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    address = models.CharField(max_length=200, blank=False, null=False)
    city = models.CharField(max_length=50, blank=False, null=False)
    state = models.CharField(max_length=50, blank=False, null=False, choices=STATE)
    # active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return '%s' %(self.user.email)

    def get_absolute_url(self):
        return reverse('dashboard:profile', kwargs={"slug": self.ref})

    def get_update_url(self):
        return reverse("dashboard:profile_update", kwargs={"slug": self.ref})


    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     ref = 10000 + self.id
    #     self.ref = 'U' + str(ref)
    #     super().save(*args, **kwargs)


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        ref = 10000 + instance.profile.id
        instance.profile.ref = 'U' + str(ref)
        instance.profile.save()
        
# post_save.connect(create_user_profile, sender=User)
# post_save.connect(save_user_profile, sender=User)






PLANS = (
    ('Free', 'Free'),
    ('Basic', 'Basic'),
    ('Standard', 'Standard'),
    ('Pro', 'Pro'),
    ('Premium', 'Premium'),
)

def extra_days():
    return timezone.now() + timedelta(days=30)

class Subscription(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, blank=True)
    plan = models.CharField(max_length=50, choices=PLANS, default='Free', null=True, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=extra_days)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return '%s' %(self.plan)


    @receiver(post_save, sender=Profile)
    def create_user_subscription(sender, instance, created, **kwargs):
        if created:
            Subscription.objects.create(user=instance)

    @receiver(post_save, sender=Profile)
    def save_user_subscription(sender, instance, **kwargs):
        if instance.subscription.end_date < timezone.now():
            instance.subscription.active = False
        else:
            instance.subscription.active = True
        instance.subscription.save()

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     if self.end_date <= timezone.now():
    #         self.active = False
    #     else:
    #         self.active = True
    #     super().save(*args, **kwargs)















# class ClientRequestQuerySet(models.query.QuerySet):
#     def active(self):
#         return self.filter(active=True)

# class ClientRequestManager(models.Manager):
    
#     def get_queryset(self):
#         return ClientRequestQuerySet(self.model, using=self._db)

#     def all(self, *args, **kwargs):
#         return self.get_queryset()

#     def get_related(self, instance):
#         qs = self.all().filter(category=instance.category).filter(property_type=instance.property_type).exclude(id=instance.id).order_by("?")#.distinct()
#         return qs

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

I_AM_AN = (
  ('Individual', 'Individual'),
  ('Agent', 'Agent'),
)


class ClientRequest(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    ref = models.CharField(max_length=30, blank=True, null=True, unique=True, editable=False)
    category = models.CharField(max_length=120, choices=CATEGORIES)
    property_type = models.CharField(max_length=120, choices=PROPERTY_TYPE)
    bedroom = models.IntegerField(null=True, blank=True, choices=NUMBER_LIST)
    budget = models.DecimalField(max_digits=20, decimal_places=2)
    country = models.CharField(max_length=50, blank=True, null=True, default='Nigeria', editable=False)
    state = models.CharField(max_length=120, null=False, blank=False, choices=STATE)
    # city = models.CharField(max_length=200, null=False, blank=False)
    locality = models.CharField(max_length=200)
    comment = models.TextField(blank=False, null=False)
    i_am_an = models.CharField(max_length=120, choices=I_AM_AN)
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=11, validators=[RegexValidator(regex='^[0-9]{11}$', message='Please enter a valid phone number', code='invalid number')])
    whatsapp = models.CharField(max_length=11, blank=True, null=True, validators=[RegexValidator(regex='^[0-9]{11}$', message='Please enter a valid phone number', code='invalid number')])
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    # objects = ClientRequestManager()

    class Meta:
        ordering = ["-timestamp", "-ref"]

    def __str__(self):
        return "%s" %(self.ref)

    def get_absolute_url(self):
        return reverse("dashboard:client_request_detail", kwargs={"slug": self.ref})

    def get_markdown(self):
        comment = self.comment
        markdown_text = markdown(comment)
        return mark_safe(markdown_text)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        ref = 10000 + self.id
        self.ref = 'R' + str(ref)
        super().save(*args, **kwargs)


# def client_request_post_save_receiver(sender, instance, *args, **kwargs):

#     ref = 10000 + instance.id
#     instance.ref = 'U' + str(ref)

# post_save.connect(client_request_post_save_receiver, sender=ClientRequest)










# class MyMessageQuerySet(models.query.QuerySet):
#     def trashed(self):
#         return self.filter(active=True)

# class MyMessageManager(models.Manager):
    
#     def get_queryset(self):
#         return MyMessageQuerySet(self.model, using=self._db)

#     def all(self, *args, **kwargs):
#         return self.get_queryset()

#     def read(self, *args, **kwargs):
#         return self.get_queryset()

#     def get_related(self, instance):
#         qs = self.all().filter(category=instance.category).filter(property_type=instance.property_type).exclude(id=instance.id).order_by("?")#.distinct()
#         return qs


class MyMessage(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    ref = models.CharField(max_length=30, blank=True, null=True, unique=True, editable=False)
    subject = models.CharField(max_length=120)
    comment = models.TextField(blank=False, null=False)
    broadcast = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    trashed = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    # objects = MyMessageManager()

    class Meta:
        ordering = ["-timestamp", "-ref"]

    def __str__(self):
        return "%s" %(self.ref)

    def get_absolute_url(self):
        return reverse("dashboard:my_message_detail", kwargs={"slug": self.ref})

    def get_markdown(self):
        comment = self.comment
        markdown_text = markdown(comment)
        return mark_safe(markdown_text)



    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        ref = 10000 + self.id
        self.ref ='M' + str(ref)
        super().save(*args, **kwargs)


# def my_message_post_save_receiver(sender, instance, *args, **kwargs):
#     ref = 10000 + instance.id
#     instance.ref = 'M' + str(ref)

# post_save.connect(my_message_post_save_receiver, sender=MyMessage)




















