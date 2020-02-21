from django.shortcuts import render

from products.models import Product
from .models import Newsletter
from .forms import NewsletterForm



def newsletter(request):
    form = NewsletterForm(request.POST or None)
    product_list = Product.objects.get_products()[:3]
    context = {
        'title': None,
		'form': form,
        'product_list': product_list,
    }
    if form.is_valid():
        form_email = form.cleaned_data.get("email")
        query = Newsletter.objects.filter(email=form_email)
        if query:
            title = "Already Subscribed"
        else:
            form.save()
            title = "Subscription Confirmed"
        context = {
            'title': title,
            'product_list': product_list,
        }
    return render(request, 'newsletter.html', context)
