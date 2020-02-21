from django.contrib import admin



from .models import Newsletter
from .forms import NewsletterForm

class NewsletterAdmin(admin.ModelAdmin):
	list_display = ["__str__", "timestamp", "updated"]
	list_filter = ["timestamp", "updated"]
	form = NewsletterForm

admin.site.register(Newsletter, NewsletterAdmin)
