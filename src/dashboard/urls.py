from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path
from .views import (
    DashboardView,
    # ProfileView,
    ProfileUpdateView,
	ProductCreateView,
	ProductUpdateView,
    ProductListView,
    ProductDeleteView,
    product_image_update,
    # ProductDetailView,
    SubscriptionView,
    ClientRequestCreateView,
    client_request_sent,
    ClientRequestDashboardCreate,
    ClientRequestUpdateView,
    ClientRequestListView,
    ClientRequestDetailView,
    ClientRequestDeleteView,
    MyMessageListView,
    MyMessageDetailView,
    MyMessageDeleteView,
    Error404View,
    # CategoryDetailView,
    # list_view,
    # detail_slug_view,
    # ProductRatingAjaxView,
    WishlistView,
    WishlistDeleteView,
    BoostedAjaxView,
    FeatureAjaxView,
    AvailableAjaxView,
    )

app_name = 'dashboard'

urlpatterns = [
    # path('category/<slug:category>/', CategoryDetailView.as_view(), name='category'),
    # path('<slug:slug>/', detail_slug_view, name='detail'),
    # path('<int:pk>/', ProductDetailView.as_view(), name='detail'),  
    # path('ajax/rating/', ProductRatingAjaxView.as_view(), name='ajax_rating'),
    path('property/<slug:slug>/image/', product_image_update, name='product_image_update'),
    path('property/<slug:slug>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('property/<slug:slug>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('property/add/', ProductCreateView.as_view(), name='product_create'),
    path('properties/', ProductListView.as_view(), name='product_list'),
    path('subscription/', SubscriptionView.as_view(), name='subscription'),
    # path('<slug:slug>/', ProfileView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('client-request/<slug:slug>/update/', ClientRequestUpdateView.as_view(), name='client_request_update'),
    path('client-request/<slug:slug>/delete/', ClientRequestDeleteView.as_view(), name='client_request_delete'),
    path('client-request/dashboard-create/', ClientRequestDashboardCreate.as_view(), name='client_request_dashboard_create'),
    path('client-request/create/', ClientRequestCreateView.as_view(), name='client_request_create'),    
    path('client-request/sent/', client_request_sent, name='client_request_sent'),
    path('client-request/<slug:slug>/', ClientRequestDetailView.as_view(), name='client_request_detail'),
    path('client-request/', ClientRequestListView.as_view(), name='client_request_list'),
    path('message/<slug:slug>/delete/', MyMessageDeleteView.as_view(), name='my_message_delete'),
    path('message/<slug:slug>/', MyMessageDetailView.as_view(), name='my_message_detail'),
    path('message/', MyMessageListView.as_view(), name='my_message_list'),
    path('wishlist/<int:pk>/delete', WishlistDeleteView.as_view(), name='wishlist_delete'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('ajax/boosted/', BoostedAjaxView.as_view(), name='ajax_product_boosted'),
    path('ajax/feature-ad/', FeatureAjaxView.as_view(), name='ajax_product_featured'),
    path('ajax/available/', AvailableAjaxView.as_view(), name='ajax_product_available'),
    path('404/', Error404View.as_view(), name='404'),
    path('home/', DashboardView.as_view(), name='home'),
]



