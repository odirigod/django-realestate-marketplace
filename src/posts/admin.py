from django.contrib import admin

# Register your models here.
from .models import Post, Category

class PostModelAdmin(admin.ModelAdmin):
	list_display = ["title", "draft", "publish", "timestamp", "updated"]
	# list_display_links = ["updated"]
	list_editable = ["draft"]
	list_filter = ["draft", "timestamp", "updated"]
	prepopulated_fields = {'slug': ('title',)}
	search_fields = ["title", "content"]
	class Meta:
		model = Post


admin.site.register(Post, PostModelAdmin)



class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'active']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['active',]
    list_editable = ['active']
    class Meta:
        model = Category

admin.site.register(Category, CategoryAdmin)
