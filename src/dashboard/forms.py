from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

# from pagedown.widgets import PagedownWidget

# from newsletter.models import Newsletter
from .models import Profile, ClientRequest







class SignupForm(forms.ModelForm):
    captcha = forms.CharField(max_length=30)

    class Meta:
      model = get_user_model()
      fields = ['first_name', 'last_name']

    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha')
        if not captcha == '4':
            raise forms.ValidationError("Your answer is incorrect.")
        return captcha

    def signup(self, request, user):
      user.first_name = self.cleaned_data['first_name']
      user.last_name = self.cleaned_data['last_name']
      user.save()




class ProfileForm(forms.ModelForm):
    # first_name = forms.CharField(label=_("First name"),
    #                            max_length=40,
    #                            widget=forms.TextInput(
    #                                attrs={'placeholder':
    #                                           _('First name'),
    #                                       'autofocus': 'autofocus'}))
    # last_name = forms.CharField(label=_("Last name"),
    #                            max_length=40,
    #                            widget=forms.TextInput(
    #                                attrs={'placeholder':
    #                                           _('Last name'),
    #                                       'autofocus': 'autofocus'}))
    # email = forms.CharField(label=_("Email address"),
    #                            max_length=50,
    #                            widget=forms.TextInput(
    #                                attrs={'placeholder':
    #                                           _('Email address'),
    #                                       'autofocus': 'autofocus'}))
    
    phone = forms.CharField(label=_("Phone number"), max_length=11)
    whatsapp = forms.CharField(label=_("WhatsApp number"), max_length=11)

    # website = forms.URLField(initial='http://')

    # company = forms.CharField(label=_("Company name"),
    #                            max_length=200,
    #                            widget=forms.TextInput(
    #                                attrs={'placeholder':
    #                                           _('Enter your company name'),
    #                                       'autofocus': 'autofocus'}))

    # country = forms.CharField(initial='Nigeria')



    class Meta:
        # model = get_user_model()
        # fields = ['first_name', 'last_name']
        model = Profile
        fields = ['image', 'phone', 'whatsapp', 'who_are_you', 'address', 'city', 'state', 'company', 'website']

    # def signup(self, request, user):
    #     user.profile.image = self.cleaned_data['image']
    #     user.profile.phone = self.cleaned_data['phone']
    #     user.profile.who_are_you = self.cleaned_data['who_are_you']
    #     user.profile.address = self.cleaned_data['address']
    #     user.profile.city = self.cleaned_data['city']
    #     user.profile.state = self.cleaned_data['state']
    #     # user.profile.country = self.cleaned_data['country']
    #     try:
    #       company = self.cleaned_data['company']
    #       if company:
    #         user.profile.company = company
    #     except:
    #       pass
        # email = self.cleaned_data['email']
        # email_exist = Newsletter.objects.filter(email=email)
        # if not email_exist:
        #   Newsletter.objects.create(email=email)

        # user.first_name = self.cleaned_data['first_name']
        # user.last_name = self.cleaned_data['last_name']
        # user.email = self.cleaned_data['email']
        # # user.username = self.cleaned_data['phone']
        # user.save()









class ClientRequestForm(forms.ModelForm):
    # category = forms.ChoiceField(label=_("Choose a category"))
    # property_type = forms.ChoiceField(label=_("Type of property"))
    # bedroom = forms.ChoiceField(label=_("Choose number of bedroom(s)"))
    name = forms.CharField(label=_("Full name"), max_length=60)
    phone = forms.CharField(label=_("Phone number"), max_length=11)
    whatsapp = forms.CharField(label=_("WhatsApp number"), max_length=11, required=False)
    email = forms.CharField(label=_("Email address"), max_length=50)
    budget = forms.DecimalField(label=_("Maximum Budget(N)"))

    class Meta:
        model = ClientRequest
        fields = ['category', 'property_type', 'bedroom', 'budget', 'state', 'locality', 'comment', 'i_am_an', 'name', 'email', 'phone', 'whatsapp']