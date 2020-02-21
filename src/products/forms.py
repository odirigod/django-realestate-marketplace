from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from .models import Product, ProductImage


class ProductForm(forms.ModelForm):
    area = forms.IntegerField(label=_("Size in square meters (sqm)"), required=False)
    # bedroom = forms.DecimalField(label=_("Choose number of bedroom(s)"))
    # name = forms.CharField(label=_("Full name"), max_length=60)
    # phone = forms.CharField(label=_("Phone number"), max_length=11)
    # whatsapp = forms.CharField(label=_("WhatsApp number"), max_length=11)
    # email = forms.CharField(label=_("Email address"), max_length=50)
    # budget = forms.DecimalField(label=_("Maximum Budget(N)"))

    class Meta:
        model = Product
        fields = ['title', 'category', 'property_type', 'price', 'address', 'state', 'city', 'description', 'area', 'bedroom', 'bathroom', 'parking']


class ProductImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image') 
    class Meta:
        model = ProductImage
        fields = ['image',]


