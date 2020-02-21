from django.contrib import admin

from .models import Product, ProductImage, Wishlist


# StackedInline
class ProductImageInline(admin.TabularInline):
	max_num = 5
	extra = 1
	model = ProductImage
	# fields = ['media']


class ProductAdmin(admin.ModelAdmin):
	list_display = ["realtor", "title", "category", "property_type", "active", "boosted", "featured", "timestamp"]
	search_fields = ["title", "description"]
	list_filter = ["active", "timestamp", "available", "featured", "boosted", "category", "property_type"]
	list_editable = ["active", "boosted", "featured"]
	inlines = [ProductImageInline]
	class Meta:
		model = Product


admin.site.register(Product, ProductAdmin) 


admin.site.register(Wishlist)
