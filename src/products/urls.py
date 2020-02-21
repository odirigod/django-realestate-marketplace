from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path
from .views import (
    # home,
    # product_add,
	# ProductCreateView,
    ProductListView,
	# ProductUpdateView,
    ProductDetailRedirect,
    ProductDetailView,
    product_detail,
    # CategoryDetailView,
    # list_view,
    # detail_slug_view,
    # ProductRatingAjaxView,
    WishlistAjaxView,
    )

app_name = 'products'

urlpatterns = [
    path('<int:pid>/', ProductDetailRedirect.as_view(), name='product_redirect'),
    path('<int:pid>/<slug:slug>/', product_detail, name='product_detail'),
    path('<int:pid>/<slug:slug>/', ProductDetailView.as_view(), name='detail'),

    # path('category/<slug:category>/', CategoryDetailView.as_view(), name='category'),
    # path('<slug:slug>/', detail_slug_view, name='detail'),
    # path('<int:pk>/', ProductDetailView.as_view(), name='detail'),
    # path('add/', product_add, name='add'),
    # path('create/', ProductCreateView.as_view(), name='product_create'),
    # path('create/', ProductCreateView.as_view(), name='create'),
    # path('<slug:slug>/edit/', ProductUpdateView.as_view(), name='update'),
    # path('ajax/rating/', ProductRatingAjaxView.as_view(), name='ajax_rating'),
    path('ajax/wishlist/', WishlistAjaxView.as_view(), name='ajax_wishlist'),
    path('', ProductListView.as_view(), name='product_list'),
    # path('', ProductListView.as_view(), name='list'),
    # path('', ProductListView, name='list'),
]



