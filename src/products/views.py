from django.conf import settings
from urllib.parse import quote_plus
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail, send_mass_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db.models import Q, Avg, Count
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
# from django.views.decorators.csrf import csrf_protect, csrf_exempt
# from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
from django.views.generic.list import ListView
from django.views.generic.base import RedirectView
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django_filters import FilterSet, CharFilter, NumberFilter

from homelink.mixins import FilterMixin, AjaxRequiredMixin
from dashboard.mixins import ProfileMixin
# from newsletter.models import Newsletter
# from dashboard.forms import ProductsInquiryForm
from .models import Product, ProductImage, Wishlist
from .forms import ProductForm, ProductImageForm







class ProductDetailRedirect(RedirectView):

    permanent = False
    query_string = True
    pattern_name = 'products:product_detail'

    def get_redirect_url(self, pid):
        product = Product.objects.get(pid=pid)
        slug = product.slug
        return reverse('products:product_detail', args=(pid, slug))



def product_detail(request, pid, slug):
    instance = Product.objects.get(pid=pid)
    context = {
        'object': instance,
        "related": sorted(Product.objects.get_related(instance)[:4], key=lambda x: random.random()),
        "product_list": Product.objects.get_products()[:3],
        "share_string": quote_plus(instance.description)
    }
    return render(request, 'products/product_detail.html', context)




# class ProductDetailView(FormMixin, DetailView):
import random
class ProductDetailView(DetailView):
    model = Product
    slug_field = "pid"
    # form_class = ProductInquiryForm
    template_name = "products/product_detail.html"
    # success_url = reverse_lazy('product:inquiry_success')   

    # def post(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     form = self.get_form()
    #     if form.is_valid():
    #         form.instance.product = instance
    #         form.instance.user = instance.user
    #         # Subscribe Client
    #         form_email = form.cleaned_data["email"]
    #         exist = Newsletter.objects.filter(email=form_email)
    #         if exist:
    #             pass
    #         else:
    #             Newsletter.objects.create(email=form_email)
    #         form.save()
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)

    # def form_valid(self, form, *args, **kwargs):
    #     fullname = form.cleaned_data["fullname"]
    #     phone = form.cleaned_data["phone"]
    #     client_email = form.cleaned_data["email"]
    #     inquiry = form.cleaned_data["message"]
    #     agent_email =  self.get_object().user.email
    #     property_pid = self.get_object() 

    #     subject = "Homelink Client Enquiry"
    #     from_email = "noreply-homelink@homelink.ng" #settings.EMAIL_HOST_USER#
    #     to_email = agent_email
    #     inquiry_message = 'Property (PID): %s \n\n Message: \n %s \n\nThank you, \n\nName: %s \nPhone: %s \nEmail: %s  \n' %(
    #         property_pid,
    #         inquiry,
    #         fullname,
    #         phone,
    #         client_email,
    #     )
    #     message1 = (subject, inquiry_message, from_email, [to_email])
    #     # Inquiry confirmation message
    #     sender_email = client_email
    #     sender_message = "Hi %s, \n\nThank you for using homelink.ng \nYour message has been received. \nThe property manager will attend to your inquiry. \n\nRegards. \nTeam Homelink.ng \n" %(fullname,)
    #     message2 = (subject, sender_message, from_email, [sender_email])
    #     send_mass_mail((message1, message2), fail_silently=False)
    #     return super(ProductDetailView, self).form_valid(form, *args, **kwargs)


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        instance = self.get_object()
        context["related"] = sorted(Product.objects.get_related(instance)[:4], key=lambda x: random.random())
        context["product_list"] = Product.objects.get_products()[:3]
        context["share_string"] = quote_plus(instance.description)
        # context["advert_image"] = FeaturedImage.objects.filter(active=True).last()
        return context


# def inquiry_success(request):
#     return render(request, 'products/inquiry_success.html', {})




class ProductFilter(FilterSet):
    state = CharFilter( field_name='state', lookup_expr='iexact', distinct=True)
    category = CharFilter( field_name='category', lookup_expr='iexact', distinct=True)
    property_type = CharFilter( field_name='property_type', lookup_expr='iexact', distinct=True)
    bedrooms = NumberFilter( field_name='bedroom', lookup_expr='exact', distinct=True)
    bathrooms = NumberFilter( field_name='bathroom', lookup_expr='exact', distinct=True)
    min_price = NumberFilter( field_name='price', lookup_expr='gte', distinct=True)
    max_price = NumberFilter( field_name='price', lookup_expr='lte', distinct=True)
    class Meta:
        model = Product
        fields = [
            'state',
            'category',
            'property_type',
            'bedrooms',
            'bathrooms',
            'price'
        ]



class ProductListView(FilterMixin, ListView): 
    model = Product
    queryset = Product.objects.get_products()#.order_by('?')
    filter_class = ProductFilter
    template_name = 'products/product_list.html' 

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['now'] = timezone.now()
        context['query'] = self.request.GET.get("q")
        context["product_list"] = Product.objects.get_products()[:3]
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)

        # paginator = Paginator(qs, 15) # show 15 products per page
        # page = self.request.GET.get('page')
        # try:
        #     qs = paginator.page(page)
        # except PageNotAnInteger:
        #     # If page is not an integer, deliver first page.
        #     qs = paginator.page(1)
        # except EmptyPage:
        #     # If page is out of range (e.g. 9999), deliver last page of results.
        #     qs = paginator.page(self.paginator.num_pages)

        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(title__icontains=query)|
                Q(description__icontains=query)|
                Q(pid__iexact=query)|
                Q(price__iexact=query)
            ).distinct()
        return qs




class WishlistAjaxView(AjaxRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({}, status=401)
        user = request.user
        product_pid = request.POST.get("product_pid")
        exists = Product.objects.filter(pid=product_pid).exists()
        if not exists:
          return JsonResponse({}, status=404)
        try:
          product_obj = Product.objects.get(pid=product_pid)
        except:
          product_obj = Product.objects.filter(pid=product_pid).first()
        # wishlist_obj, wishlist_obj_created = Wishlist.objects.get_or_create(user=user, product=product_obj)

        try:
            wishlist_obj = Wishlist.objects.get(user=user, product=product_obj)
        except:
            wishlist_obj = Wishlist.objects.filter(user=user, product=product_obj).first()
        if wishlist_obj:
            return JsonResponse({}, status=422)
        else:
        # except:
            # rating_obj = ProductRating.objects.create(user=user, product=product_obj)
            wishlist_obj = Wishlist()
            wishlist_obj.user = user
            wishlist_obj.product = product_obj
        wishlist_obj.save()

        data = {
            "success": True,
        }
        return JsonResponse(data, status=200)































# class ProductCreateView(ProfileMixin, CreateView):
#     model = Product
#     form_class = ProductForm
#     template_name = "dashboard/property_form.html"
#     success_url = reverse_lazy('dashboard:listing')
#     submit_btn = "Add Product"

#     def form_valid(self, form):
#         realtor = self.get_account()
#         form.instance.realtor = realtor
#         valid_data = super().form_valid(form)
#         return valid_data





# from django.forms import modelformset_factory
# from django.template import RequestContext


# @login_required
# def product_add(request):

#     ImageFormSet = modelformset_factory(ProductImage,
#                                         form=ProductImageForm, extra=6)

#     if request.method == 'POST':

#         postForm = ProductForm(request.POST)
#         formset = ImageFormSet(request.POST, request.FILES,
#                                queryset=ProductImage.objects.none())

#         if postForm.is_valid() and formset.is_valid():
#             post_form = postForm.save(commit=False)
#             post_form.realtor = request.user.profile
#             post_form.save()

#             for form in formset.cleaned_data:
#                 try:
#                     image = form['image']
#                     photo = ProductImage(product=post_form, image=image)
#                     photo.save()
#                 except:
#                     pass
#             messages.success(request, "Yeeew, Your property is successfully added!")
#             return HttpResponseRedirect("/dashboard/listing/")
#         else:
#             print (postForm.errors, formset.errors)
#     else:
#         postForm = ProductForm()
#         formset = ImageFormSet(queryset=ProductImage.objects.none())
#     return render(request, 'dashboard/property_form_create.html', 
#                   {'postForm': postForm, 'formset': formset})










# class ProductUpdateView(ProfileMixin, UpdateView):
#     model = Product
#     form_class = ProductForm
#     slug_field = 'pid'
#     template_name = "dashboard/property_form_update.html"
#     success_url = reverse_lazy('dashboard:listing')
#     submit_btn = "Update Product"
#     ImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, max_num=6, extra=6)

#     def get_initial(self):
#         initial = super(ProductUpdateView, self).get_initial()
#         return initial


#     def post(self, request, *args, **kwargs):
#         # ImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, extra=6)
#         self.object = self.get_object()
#         postForm = self.get_form()
#         formset = self.ImageFormSet(self.request.POST, self.request.FILES, queryset=ProductImage.objects.filter(product=self.get_object()))

#         if postForm.is_valid() and formset.is_valid():
#             post_form = postForm.save(commit=False)
#             post_form.realtor = request.user.profile
#             # post_form.save()
#             # ProductImage.objects.filter(product=post_form, image=image).delete()
#             for form in formset.cleaned_data:
#                 try:
#                     image = form['image']
#                     if image:
#                         # image_id = form['id']
#                         # exist = ProductImage.objects.filter(product=post_form, image=image)
#                         # if exist:
#                         #     exist.delete()                    
#                         photo = ProductImage(product=post_form, image=image)
#                         photo.save()
#                 except:
#                     pass
#             messages.success(request, "Your property is successfully updated")
#             # return super(ProductUpdateView, self).post(request, *args, **kwargs)#self.form_valid(postForm) #HttpResponseRedirect("/")
#         # else:
#             # print (postForm.errors, formset.errors)
#             return self.form_valid(postForm)
#         else:
#             return self.form_invalid(postForm)        

#     def form_valid(self, *args, **kwargs):
#         valid_data = super(ProductUpdateView, self).form_valid(*args, **kwargs)
#         return valid_data

#     def get_context_data(self, *args, **kwargs):
#         context = super(ProductUpdateView, self).get_context_data(*args, **kwargs)
#         context["postForm"] = self.get_form()
#         context["formset"] = self.ImageFormSet(queryset=ProductImage.objects.filter(product=self.get_object()))
#         return context





# class ProductDelete(ProfileMixin, DeleteView):
#     model = Product
#     slug_field = 'pid'
#     template_name = "dashboard/property_confirm_delete.html"
#     success_url = reverse_lazy('dashboard:listing')













