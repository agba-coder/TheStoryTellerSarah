
from django.http import HttpResponse

from django.shortcuts import render, redirect, get_object_or_404
from .models import *

from django.contrib import messages
from django.conf import settings

from django.contrib.sites.shortcuts import get_current_site

from django.core.mail import send_mail, BadHeaderError

from django.contrib.gis.geoip2 import GeoIP2
from django.db.models import Q

from django.contrib.auth.decorators import login_required 

import random
# import requests
# import json

import socket

from decouple import config

# importing all models from DB in the models.py file
from blog.models import Post, Comment, Category, Newsletter, ReceivedMail, SocialLink, Visitor

# importing the form for commenting from the blog/forms.py file
from .forms import CommentForm


from weblog.urls import sitemaps

# getting current domain name or current hostname
site = get_current_site

# Create your views here.

def handler400(request, exception):
    categories = Category.objects.filter().order_by("date_created").values()
    categories = categories [:3]
    context = {"categories": categories, "site": site}
    return render(request, "error_pages/400.html", context, status=400)


def handler403(request, exception):
    categories = Category.objects.filter().order_by("date_created").values()
    categories = categories [:3]
    context = {"categories": categories, "site": site}
    return render(request, "error_pages/403.html", context, status=403)

def handler404(request, exception):
    categories = Category.objects.filter().order_by("date_created").values()
    categories = categories [:3]
    context = {"categories": categories, "site": site}
    return render(request, "error_pages/404.html", context, status=404)


def handler500(request):
    categories = Category.objects.filter().order_by("date_created").values()
    categories = categories [:3]
    context = {"categories": categories, "site": site}
    return render(request, "error_pages/500.html", context, status=500)


# view function for home url
def home(request):

    # Get visitor's IP address
    ip_address = request.META.get('REMOTE_ADDR')
    print(ip_address)

    # Get visitor's location information
    g = GeoIP2()
    try:
        city = g.city(ip_address)['city']
        country = g.country(ip_address)['country_name']
    except:
        city = "Unknown"
        country = "Unknown"


    if request.method == "POST":
        email = request.POST["email"]

        newsletter = Newsletter.objects.update_or_create(subscribed_email_address=email)


    x = Post.objects.filter(status=Post.ACTIVE)
    # x = Post.objects.all().order_by('-date_created').values()


    # added all the blog posts from the DB to a list
    trending = x[:1]
    random_posts = x[:4]
    topPosts = x[4:7]

    # trending = trending[::4]

    # this line of code is to display the categories from  the DB to the website
    categories = Category.objects.filter().order_by("date_created").values()
    categories = categories [:3]

    context = {x :'posts', 'rand_posts': random_posts, "trending_post": trending, "categories": categories, "site": site}
    return render(request, 'blog/home.html', context)


# view function for blog posts
@login_required(login_url="/accounts/auth/login", redirect_field_name='next')
def blog_post(request, category_slug, slug):

    instagram_url = SocialLink.objects.get(social_media="Instagram").link

    post = get_object_or_404(Post, slug=slug, status=Post.ACTIVE)

    data = Post.objects.filter(status=Post.ACTIVE).order_by('-date_created').values()

    recent_posts = data[:4]
    print(recent_posts[1])
    previous_posts = data[3:]

    categories = Category.objects.filter().order_by("date_created").values()
    categories = categories [:3]


    # Get visitor's IP address
    ip_address = request.META.get('REMOTE_ADDR')
    print(ip_address)

    # Get visitor's location information
    g = GeoIP2()
    try:
        city = g.city(ip_address)['city']
        country = g.country(ip_address)['country_name']
    except:
        city = "Unknown"
        country = "Unknown"


    # Check if the reader has already been tracked for this blog post
    if not Visitor.objects.filter(ip_address=ip_address, blog_post=post).exists():

    # If not, create a new Reader entry to track the reader and Save the visitor information to the database
        visitor = Visitor.objects.create(ip_address=ip_address, city=city, country=country, blog_post=post)
        print(visitor)

    # Get the total number of visitors
    total_visitors = Visitor.objects.count()


    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

            return redirect("blog_post", category_slug=category_slug, slug=slug)

        else:
            form = CommentForm()


    context = {'post': post, "recent_posts": recent_posts, "previous_posts": previous_posts, "form": form, "categories": categories, "site": site, "url": instagram_url, "visitors": total_visitors}
    return render(request, 'blog/blog-post.html', context)


# view function for categories
# @login_required(login_url="/accounts/auth/login", redirect_field_name='next')
def category(request, slug):
    if not request.user.is_authenticated:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
        
    category = get_object_or_404(Category, slug=slug)

    posts = category.posts.filter(status=Post.ACTIVE)

    categories = Category.objects.filter().order_by("date_created").values()
    categories = categories [:3]

    return render(request, "blog/category.html", {'category': category, 'posts': posts, "categories": categories, "site": site})



# view function for search
def search(request):
    query = request.GET.get('query', '')

    posts = Post.objects.filter(status=Post.ACTIVE).filter(Q(title__icontains=query) | Q(intro__icontains=query) | Q(body__icontains=query))

    categories = Category.objects.filter().order_by("date_created").values()
    categories = categories [:3]

    return render(request, 'blog/search.html', {"posts": posts, "query": query, "categories": categories, "site": site})



# view function for contact
def contact(request):

    if request.method == "POST":
        name = request.POST["name"]
        subject = request.POST["subject"]
        from_email = request.POST["email"]
        phone = request.POST["phone"]
        payload = request.POST["message"]

        mail = ReceivedMail.objects.create(name=name, subject=subject, email=from_email, phone=phone, message=payload)
        mail.save()

        subject = "✅ Hi TheStoryTellerSarah, you've a new message from your blog!"
        message = f"Name: {name}\nPhone: {phone}\nEmail Address: {from_email}.\nMessage: \n{payload}"
        EMAIL_HOST = settings.EMAIL_HOST_USER

        try:
            send_mail(subject, message, from_email, ["hi.thestorytellersarah@gmail.com", "hi.agbacoder@gmail.com"])
            messages.success(request, "Your Message Has Been Sent ✅!")
            return redirect("contact")
        except BadHeaderError:
            message.error(request, "❌ Oops, An Error Occurred. Please Try Again!")
            return render(request, "blog/contact.html")

    categories = Category.objects.filter().order_by("date_created").values()
    categories = categories [:3]
    context = {"categories": categories, "site": site}
    return render(request, 'blog/contact.html', context)


# view function for robot_txt
def robot_txt(request):
    text = [
        "User-Agent: *",
        "Disallow: /admin/",
    ]
    return HttpResponse("\n".join(text), content_type="text/plain")


