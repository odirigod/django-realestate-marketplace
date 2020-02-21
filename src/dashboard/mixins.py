import datetime
from django.db.models import Count, Min, Sum, Avg, Max
from django.http import Http404

from homelink.mixins import LoginRequiredMixin
from products.models import Product 

from .models import Profile

# from django.dispatch import receiver
# from ravepay.signals import payment_verified


class ProfileMixin(LoginRequiredMixin, object):
    account = None
    properties = []
    transactions = []

    def get_account(self):
        user = self.request.user
        accounts = Profile.objects.filter(user=user)
        # to get managers account user >>> accounts = RealtorAccount.objects.filter(managers_in=user)
        if accounts.exists() and accounts.count() == 1:
            self.account = accounts.first()
            return accounts.first()
        return None

    # def get_properties(self):
    #     account = self.get_account()
    #     properties = Properties.objects.filter(realtor=account)
    #     self.properties = properties
    #     return properties

    # def get_variations(self):
    #     properties = self.get_properties()
    #     variations = Variation.objects.filter(product__in=properties)
    #     self.variations = variations
    #     return variations

    # def get_transactions(self):
    #     variations = self.get_variations()
    #     transactions = Sale.objects.filter(variation__in=variations)
    #     return transactions

    # def get_transactions_today(self):
    #     today = datetime.date.today()
    #     today_min = datetime.datetime.combine(today, datetime.time.min)
    #     today_max = datetime.datetime.combine(today, datetime.time.max)
    #     return self.get_transactions().filter(timestamp__range=(today_min, today_max))

    # def get_total_sales(self):
    #     transactions = self.get_transactions().aggregate(Sum("total_price"))
    #     total_sales = transactions["total_price__sum"]
    #     return total_sales

    # def get_today_sales(self):
    #     transactions = self.get_transactions_today().aggregate(Sum("total_price"))
    #     total_sales = transactions["total_price__sum"]
    #     return total_sales





class OwnerMixin(LoginRequiredMixin, object):
    def get_object(self, *args, **kwargs):
        user = self.request.user.profile
        obj = super().get_object(*args, **kwargs)
        if obj.user == user:
            return obj
        else:
            raise Http404




class MessageOwnerMixin(LoginRequiredMixin, object):
    def get_object(self, *args, **kwargs):
        user = self.request.user.profile
        obj = super().get_object(*args, **kwargs)
        if obj.receiver == user or obj.broadcast == True:
            return obj
        else:
            raise Http404












# @receiver(payment_verified)
# def on_payment_verified(sender, ref, amount, **kwargs):
#     """
#     ref: paystack reference sent back.
#     amount: amount in Naira or the currency passed
#     """
#     pass