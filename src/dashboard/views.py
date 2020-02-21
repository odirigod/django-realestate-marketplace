import random
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View 
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
from django.views.generic.list import ListView
from django.urls import reverse, reverse_lazy
from django.forms import inlineformset_factory 
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from homelink.mixins import (
    LoginRequiredMixin,
    StaffRequiredMixin,
    MultiSlugMixin,
    FilterMixin,
    AjaxRequiredMixin
    )

from products.mixins import ProductOwnerMixin
from products.forms import ProductForm
from products.models import Product, ProductImage, Wishlist

from .mixins import ProfileMixin, OwnerMixin, MessageOwnerMixin
from .models import Profile, ClientRequest, MyMessage
from .forms import SignupForm, ProfileForm, ClientRequestForm 





class DashboardView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "dashboard/home.html"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(**kwargs)
        product = Product.objects.filter(realtor=self.request.user.profile)
        query = self.request.GET.get("search")
        if query:
            qs = product.filter(
                    Q(title__icontains=query)|
                    Q(category__icontains=query)|
                    Q(description__icontains=query)
                ).distinct()
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["today"] = timezone.now()
        return context



class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile 
    form_class = ProfileForm
    template_name = "dashboard/profile_update.html"
    success_url = reverse_lazy('dashboard:profile_update')
    submit_btn = "Update Profile"

    def get_object(self, queryset=None):
        return self.request.user.profile

    def form_valid(self, form):
        valid_data = super().form_valid(form)
        messages.success(self.request, "Profile updated successfully!")
        return valid_data

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["today"] = timezone.now()
        return context




class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = "dashboard/product_create.html"
    form_class = ProductForm 

    def form_valid(self, form):
        user = self.request.user.profile
        form.instance.realtor = user
        valid_data = super().form_valid(form)
        messages.success(self.request, "Property has been added.")
        return valid_data

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["today"] = timezone.now()
        return context

    def get_success_url(self):
        pid = self.object.pid
        return reverse("dashboard:product_image_update", args=[pid])



class ProductUpdateView(ProductOwnerMixin, UpdateView):
    model = Product
    form_class = ProductForm 
    slug_field = 'pid'
    template_name = "dashboard/product_update.html"
    success_url = reverse_lazy('dashboard:product_list')
    submit_btn = "Update Product"

    def form_valid(self, form):
        valid_data = super().form_valid(form)
        messages.success(self.request, "Property updated!")
        obj = self.get_object()
        return valid_data

 

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "dashboard/product_list.html"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(**kwargs)
        qs = Product.objects.filter(realtor=self.request.user.profile)
        query = self.request.GET.get("search")
        if query:
            qs = qs.filter(
                    Q(pid__iexacts=query)|
                    Q(title__icontains=query)|
                    Q(category__icontains=query)|
                    Q(property_type__icontains=query)|
                    Q(description__icontains=query)
                ).distinct()
        paginator = Paginator(qs, 10) # show 10 propertiess per page
        page = self.request.GET.get('page')
        qs = paginator.get_page(page)
        return qs


class ProductDeleteView(ProductOwnerMixin, DeleteView):
    model = Product
    slug_field = 'pid'
    success_url = reverse_lazy('dashboard:product_list')
    template_name = "dashboard/product_confirm_delete.html"



method_decorator(login_required)
def product_image_update(request, slug):
    obj = Product.objects.get(pid=slug)
    # obj = get_object_or_404(Product, pid=slug)
    ThumbnailInlineFormSet = inlineformset_factory(Product, ProductImage, fields=('media',), max_num=5, extra=5)
    if request.method == "POST":
        formset = ThumbnailInlineFormSet(request.POST, request.FILES, instance=obj)
        if formset.is_valid():
            formset.save()         
            messages.success(request, "Property Images updated!")
            return HttpResponseRedirect('/dashboard/properties/') #reverse('dashboard:product_list')
    else:
        formset = ThumbnailInlineFormSet(instance=obj)
    context = {
        'formset': formset
    }
    return render(request, 'dashboard/product_image_update.html', context)




class SubscriptionView(ProfileMixin, FormMixin, View):
    model = Profile

    def get(self, request, *args, **kwargs):
        account = self.get_account()
        context = {}
        context["profile"] = account 
        return render(request, "dashboard/subscription.html", context)




class ClientRequestCreateView(LoginRequiredMixin, CreateView):
    model = ClientRequest
    form_class = ClientRequestForm 
    template_name = "dashboard/client_request_create.html" 
    success_url = reverse_lazy('dashboard:client_request_sent')

    def form_valid(self, form):
        user = self.request.user.profile
        form.instance.user = user
        valid_data = super().form_valid(form)
        messages.success(self.request, "Property Request sent!")
        return valid_data

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["product_list"] = Product.objects.get_products()[:3]
        return context



def client_request_sent(request):
    contact_title = 'Request Sent Successfully'
    context = {
        "product_list": Product.objects.get_products()[:3],
    }
    return render(request, "dashboard/client_request_sent.html", context)




class ClientRequestDashboardCreate(LoginRequiredMixin, CreateView):
    model = ClientRequest
    form_class = ClientRequestForm 
    template_name = "dashboard/client_request_create_dashboard.html" 

    def form_valid(self, form):
        user = self.request.user.profile
        form.instance.user = user
        valid_data = super().form_valid(form)
        messages.success(self.request, "Property Request sent!")
        return valid_data

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["product_list"] = Product.objects.get_products()[:3]
        return context

    def get_success_url(self):
        ref = self.object.ref
        return reverse("dashboard:client_request_detail", kwargs={"slug": ref})



class ClientRequestUpdateView(OwnerMixin, UpdateView):
    model = ClientRequest
    form_class = ClientRequestForm
    slug_field = 'ref'
    template_name = "dashboard/client_request_create.html"
    success_url = reverse_lazy('dashboard:client_request_detail')
    submit_btn = "Update Request"

    def form_valid(self, form):
        valid_data = super().form_valid(form)
        messages.success(self.request, "Request updated!")
        obj = self.get_object()
        return valid_data

    def get_success_url(self):
        obj = self.get_object()
        ref = obj.ref
        return reverse("dashboard:client_request_detail", kwargs={"slug": ref})



class ClientRequestListView(LoginRequiredMixin, ListView):
    model = ClientRequest
    template_name = "dashboard/client_request_list.html"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(**kwargs)
        qs = ClientRequest.objects.all()
        query = self.request.GET.get("search")
        if query:
            qs = qs.filter(
                    Q(ref__iexacts=query)|
                    Q(category__icontains=query)|
                    Q(state__icontains=query)|
                    Q(locality__icontains=query)|
                    Q(comment__icontains=query)
                ).distinct()
        paginator = Paginator(qs, 12) # show 12 propertiess per page
        page = self.request.GET.get('page')
        qs = paginator.get_page(page)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["today"] = timezone.now()
        return context



import random
class ClientRequestDetailView(LoginRequiredMixin, DetailView):
    model = ClientRequest
    slug_field = "ref"
    template_name = "dashboard/client_request_detail.html"



class ClientRequestDeleteView(OwnerMixin, DeleteView):
    model = ClientRequest
    slug_field = 'ref'
    success_url = reverse_lazy('dashboard:client_request_list')
    template_name = "dashboard/client_request_confirm_delete.html"





class MyMessageListView(LoginRequiredMixin, ListView):
    model = MyMessage
    template_name = "dashboard/my_message_list.html"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(**kwargs)
        qs = MyMessage.objects.filter(Q(receiver=self.request.user.profile)|Q(broadcast=True)).distinct()
        query = self.request.GET.get("search")
        if query:
            qs = qs.filter(
                    Q(ref__iexacts=query)|
                    Q(sender__iexacts=query)|
                    Q(subject__icontains=query)|
                    Q(comment__icontains=query)
                ).distinct()
        paginator = Paginator(qs, 10) # show 10 propertiess per page
        page = self.request.GET.get('page')
        qs = paginator.get_page(page)
        return qs



import random
class MyMessageDetailView(MessageOwnerMixin, DetailView):
    model = MyMessage
    slug_field = "ref"
    template_name = "dashboard/my_message_detail.html"  



class MyMessageDeleteView(MessageOwnerMixin, DeleteView):
    model = MyMessage
    slug_field = 'ref'
    success_url = reverse_lazy('dashboard:my_message_list')
    template_name = "dashboard/my_message_confirm_delete.html"




class WishlistView(LoginRequiredMixin, ListView):
    model = Wishlist
    template_name = "dashboard/wishlist.html"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(**kwargs)
        qs = Wishlist.objects.filter(user=self.request.user)
        paginator = Paginator(qs, 12) # show 12 propertiess per page
        page = self.request.GET.get('page')
        qs = paginator.get_page(page)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["product_list"] = Product.objects.get_products().order_by("?")
        return context


class WishlistDeleteView(LoginRequiredMixin, DeleteView):
    model = Wishlist
    success_url = reverse_lazy('dashboard:wishlist')
    def get(self, request, *args, **kwargs):
        messages.success(self.request, "Property removed successfully!")
        return self.post(request, *args, **kwargs)






class BoostedAjaxView(AjaxRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({}, status=401)
        realtor = request.user.profile
        pid = request.POST.get("product_pid")
        exists = Product.objects.filter(pid=pid).exists()
        if not exists:
          return JsonResponse({}, status=404)
        try:
          product_obj = Product.objects.get(pid=pid)
        except:
          product_obj = Product.objects.filter(pid=pid).first()
        if not product_obj.realtor == realtor:
            return JsonResponse({}, status=403)
        if product_obj.boosted == True:
            return JsonResponse({}, status=422)
        products_boosted = Product.objects.filter(realtor=realtor, boosted=True)
        if products_boosted.exists():            
            return JsonResponse({}, status=424)
        product_obj.boosted = True
        product_obj.save()

        data = {
            "success": True,
        }
        return JsonResponse(data, status=200)




class FeatureAjaxView(AjaxRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({}, status=401)
        realtor = request.user.profile
        pid = request.POST.get("product_pid")
        exists = Product.objects.filter(pid=pid).exists()
        if not exists:
          return JsonResponse({}, status=404)
        try:
          product_obj = Product.objects.get(pid=pid)
        except:
          product_obj = Product.objects.filter(pid=pid).first()
        if not product_obj.realtor == realtor:
            return JsonResponse({}, status=403)
        if product_obj.featured == True:
            return JsonResponse({}, status=422)
        products_featured = Product.objects.filter(realtor=realtor, featured=True)
        if products_featured.exists():            
            return JsonResponse({}, status=424)
        product_obj.featured = True
        product_obj.save()

        data = {
            "success": True,
        }
        return JsonResponse(data, status=200)




class AvailableAjaxView(AjaxRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({}, status=401)
        realtor = request.user.profile
        pid = request.POST.get("product_pid")
        exists = Product.objects.filter(pid=pid).exists()
        if not exists:
          return JsonResponse({}, status=404)
        try:
          product_obj = Product.objects.get(pid=pid)
        except:
          product_obj = Product.objects.filter(pid=pid).first()
        if not product_obj.realtor == realtor:
            return JsonResponse({}, status=403)

        if product_obj.available == True:
            product_obj.available = False
        else:
            product_obj.available = True
        product_obj.save()

        data = {
            "success": True,
            "available": product_obj.available,
            "pid": product_obj.pid
        }
        return JsonResponse(data, status=200)









class Error404View(ProfileMixin, FormMixin, View):
    model = Profile

    def get(self, request, *args, **kwargs):
        # apply_form = self.get_form()
        account = self.get_account()
        context = {}
        context["profile"] = account 
        return render(request, "404.html", context)
