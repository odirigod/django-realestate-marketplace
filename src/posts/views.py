try:
    from urllib import quote_plus #python 2
except:
    pass

try:
    from urllib.parse import quote_plus #python 3
except:
    pass

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from products.models import Product
from comments.forms import CommentForm
from comments.models import Comment
from .forms import PostForm
from .models import Post, Category



def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		# message success
		messages.success(request, "Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"form": form,
	}
	return render(request, "posts/post_form.html", context)



def post_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    if instance.publish > timezone.now().date() or instance.draft:
    	if not request.user.is_staff or not request.user.is_superuser:
    		raise Http404
    share_string = quote_plus(instance.content)

    initial_data = {
    		"content_type": instance.get_content_type,
    		"object_id": instance.id
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get("content")
        fullname = form.cleaned_data.get("fullname")
        email = form.cleaned_data.get("email")
        parent_obj = None
        try:
        	parent_id = int(request.POST.get("parent_id"))
        except:
        	parent_id = None

        if parent_id:
        	parent_qs = Comment.objects.filter(id=parent_id)
        	if parent_qs.exists() and parent_qs.count() == 1:
        		parent_obj = parent_qs.first()


        new_comment, created = Comment.objects.get_or_create(
        					# user = request.user,
        					content_type= content_type,
        					object_id = obj_id,
        					content = content_data,
                            fullname = fullname,
                            email = email,
        					parent = parent_obj,
        				)
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())



    comments = instance.comments
    context = {
    	"title": instance.title,
    	"instance": instance,
    	"share_string": share_string,
    	"comments": comments,
    	"comment_form":form,
        "categories": Category.objects.filter(active=True),
        "product_list": Product.objects.get_products()[:3]
    }
    return render(request, "posts/post_detail.html", context)



def post_list(request):
    today = timezone.now().date()
    qs = Post.objects.active() #.order_by("-timestamp")
    categories = Category.objects.filter(active=True)
    if request.user.is_staff or request.user.is_superuser:
    	qs = Post.objects.all() 
    qs_list = qs
    # FILTERING CATEGORY
    writer = request.GET.get("u")
    if writer: 
        qs = qs.filter(user__username__iexact=writer)

    query = request.GET.get("q")
    if query:
    	qs = qs.filter(
    			Q(title__icontains=query)|
    			Q(content__icontains=query)|
    			Q(user__first_name__icontains=query) |
    			Q(user__last_name__icontains=query)
    			).distinct()
    paginator = Paginator(qs, 3) # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
    	queryset = paginator.page(page)
    except PageNotAnInteger:
    	# If page is not an integer, deliver first page.
    	queryset = paginator.page(1)
    except EmptyPage:
    	# If page is out of range (e.g. 9999), deliver last page of results.
    	queryset = paginator.page(paginator.num_pages)

    context = {
    	"queryset": queryset,
        "qs_list": qs_list.exclude(),
    	# "title": "List",
    	"page_request_var": page_request_var,
    	"today": today,
        "categories": categories,
        "product_list": Product.objects.get_products()[:3]
    }
    return render(request, "posts/post_list.html", context)





def post_update(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title": instance.title,
		"instance": instance,
		"form":form,
	}
	return render(request, "posts/post_form.html", context)



def post_delete(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	instance.delete()
	messages.success(request, "Successfully deleted")
	return redirect("posts:list")



def category_post_list(request, slug):
    today = timezone.now().date()
    instance = get_object_or_404(Category, slug=slug)
    qs = Post.objects.filter(category=instance) #.order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
    	# qs = Post.objects.all()
        qs = Post.objects.filter(category=instance)
    query = request.GET.get("q")
    if query:
    	qs = qs.filter(
    			Q(title__icontains=query)|
    			Q(content__icontains=query)|
    			Q(user__first_name__icontains=query) |
    			Q(user__last_name__icontains=query)
    			).distinct()
    paginator = Paginator(qs, 4) # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
    	queryset = paginator.page(page)
    except PageNotAnInteger:
    	# If page is not an integer, deliver first page.
    	queryset = paginator.page(1)
    except EmptyPage:
    	# If page is out of range (e.g. 9999), deliver last page of results.
    	queryset = paginator.page(paginator.num_pages)

    context = {
    	"queryset": queryset,
    	"title": "List",
    	"page_request_var": page_request_var,
    	"today": today,
        "categories": Category.objects.filter(active=True),
        "product_list": Product.objects.get_products()[:3]
    }
    return render(request, "posts/post_list.html", context)
