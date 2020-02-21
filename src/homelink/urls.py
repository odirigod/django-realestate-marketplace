"""homelink URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from .sitemaps import StaticViewSitemap, ProductSitemap

from contact.views import contact, contact_sent
from newsletter.views import newsletter
from .views import HomeView, about, terms, privacy, careers, advert

sitemaps = {
    'pages': StaticViewSitemap,
    'prop': ProductSitemap,
}



urlpatterns = [ 
    path('about/', about, name='about'),
    path('advert/', advert, name='advert'),
    path('careers/', careers, name='careers'),
    path('contact/', contact, name='contact'),
    path('contact/sent/', contact_sent, name='contact_sent'),  
    path('newsletter/', newsletter, name='newsletter'),
    path('posts/', include('posts.urls', namespace='posts')),
    path('privacy/', privacy, name='privacy'),
    path('terms/', terms, name='terms'),

    url(r'^sitemap\.xml', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    
    path('hl/admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')), 
    path('properties/', include('products.urls', namespace='products')),

    path('', HomeView.as_view(), name='home'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

