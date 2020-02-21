# sitemaps.py
from django.contrib import sitemaps
from django.urls import reverse
from datetime import datetime

from products.models import Product

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['about', 'terms', 'privacy', 'careers', 'advert', 'contact']
        
    def lastmod(self, item):
        return datetime.now()

    def location(self, item):
        return reverse(item)


class ProductSitemap(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 1.0

    def items(self):
        return Product.objects.filter(active=True)

    def lastmod(self, obj):
        return obj.timestamp

    def location(self, obj):
        return '/'