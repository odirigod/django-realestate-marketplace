import random
from django.views.generic import View 
from django.views.generic.base import TemplateView
from django.shortcuts import render

from products.models import Product




class HomeView(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_list'] = Product.objects.get_products().filter(featured=True).order_by("?")[:9]
        context['product_list'] = Product.objects.get_products()[:3]
        return context



def about(request):
    context = {
        "product_list": Product.objects.get_products()[:3],
    }
    return render(request, 'about.html', context)



def terms(request):
    context = {
        "product_list": Product.objects.get_products()[:3],
    }
    return render(request, 'terms.html', context)



def privacy(request):
    context = {
        "product_list": Product.objects.get_products()[:3],
    }
    return render(request, 'privacy.html', context)



def advert(request):
    context = {
        "product_list": Product.objects.get_products()[:3]
    }
    return render(request, 'advert.html', context)



def careers(request):
    context = {
        "product_list": Product.objects.get_products()[:3]
    }
    return render(request, 'careers.html', context)


