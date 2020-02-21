from django.contrib import admin

from .models import Profile, Subscription, ClientRequest, MyMessage




class SubscriptionInline(admin.TabularInline):
    model = Subscription
    extra = 0
    max_num = 1

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'ref', 'phone', 'company', 'who_are_you', 'city', 'state']
    list_filter = ['timestamp', 'user__is_active', 'user__profile__subscription__end_date', 'who_are_you', 'state']
    list_editable = []
    inlines = [
        SubscriptionInline,
    ]
    class Meta:
        model = Profile

admin.site.register(Profile, ProfileAdmin)



admin.site.register(ClientRequest)

admin.site.register(MyMessage)


