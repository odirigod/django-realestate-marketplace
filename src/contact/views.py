from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect


from products.models import Product
from .forms import ContactForm


def contact(request):
    queryset = Product.objects.get_products()
    c_form = ContactForm(request.POST or None)

    if request.method == "POST":
        if c_form.is_valid():
            form_fullname = c_form.cleaned_data.get("fullname")
            form_phone = c_form.cleaned_data.get("phone")
            form_email = c_form.cleaned_data.get("email")
            form_subject = c_form.cleaned_data.get("subject")
            form_message = c_form.cleaned_data.get("message")

            subject = 'Contact form message: %s' %(form_subject)
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = ['contact@homelink.ng']
            contact_message = " Name: %s \n Phone: %s \n Email: %s \n\n Message: \n\n %s" %(
            	form_fullname,
                form_phone,
            	form_email,
            	form_message)

            send_mail(subject,
            	contact_message,
            	from_email,
            	to_email,
            	fail_silently=True)
            context = {
            	"object_list": queryset,
            	"c_form": c_form,
            }
            return HttpResponseRedirect('/contact/sent/')

    form_fullname = request.POST.get('fullname', '')
    form_phone = request.POST.get('phone', '')
    form_email = request.POST.get('email', '')
    form_subject = request.POST.get('subject', '')
    form_message = request.POST.get('message', '')

    context = {
    	"object_list": queryset,
    	"c_form": c_form,
    	"fullname": form_fullname,
        "phone": form_phone,
    	"email": form_email,
    	"subject": form_subject,
    	"message": form_message,
        "product_list": Product.objects.get_products()[:3],
    }
    return render(request, "contact/contact.html", context)


def contact_sent(request):
	queryset = Product.objects.get_products()
	c_form = ContactForm(request.POST or None)
	contact_title = 'Message Sent Successfully'
	context = {
		"object_list": queryset,
		"c_form": c_form,
        "product_list": Product.objects.get_products()[:3],
	}
	return render(request, "contact/contact_sent.html", context)





