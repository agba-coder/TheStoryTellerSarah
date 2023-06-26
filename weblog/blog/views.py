
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from .models import *

from django.contrib import messages
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site

from django.core.mail import send_mail, BadHeaderError


from django.db.models import Q

import random
import requests
import json

import socket

from decouple import config

# importing all models from DB in the models.py file
from blog.models import Post, Comment, Category, Newsletter, PeopleWhoVistedYourSite, ReceivedMail

# importing the form for commenting from the blog/forms.py file
from .forms import CommentForm


from weblog.urls import sitemaps

# getting current domain name or current hostname
site = get_current_site

# Create your views here.

def handler400(request, exception):
    categories = Category.objects.all()
    context = {"categories": categories, "site": site}
    return render(request, "error_pages/400.html", context, status=400)


def handler403(request, exception):
    categories = Category.objects.all()
    context = {"categories": categories, "site": site}
    return render(request, "error_pages/403.html", context, status=403)

def handler404(request, exception):
    categories = Category.objects.all()
    context = {"categories": categories, "site": site}
    return render(request, "error_pages/404.html", context, status=404)


def handler500(request):
    categories = Category.objects.all()
    context = {"categories": categories, "site": site}
    return render(request, "error_pages/500.html", context, status=500)


# view function for home url
def home(request):
    
    if request.method == "POST":
        email = request.POST["email"]
        
        newsletter = Newsletter.objects.update_or_create(subscribed_email_address=email)
        # newsletter.save()
        
        
    # Your API key, available from your account page
    API_KEY = config("GEOLOCATOR_API_KEY")

    # URL to send the request to
    request_url = 'https://ipgeolocation.abstractapi.com/v1/?api_key=' + API_KEY
    # response = requests.get(request_url)
    # result = json.loads(response.content)
    # print(result)
    # print("")
    # print('ip_address: {}'.format(result['ip_address']))
    # print('City: {}'.format(result['city']))
    # print('Country: {}'.format(result['country']))
    ip = socket.gethostbyname(socket.gethostname())
    print(ip)
    
    # for ipAddress in PeopleWhoVistedYourSite.objects.all().get("ip_address").values():
    #     print(ipAddress)
        # address = People_Who_Visted_Your_Site.objects.get_or_create(ip_address=ip)
    # print()

    # response = requests.get("https://scrape.abstractapi.com/v1/?api_key=951185fac9874ba19a996902e7bb86f9&url=https://wordpress.com/read/feeds/125610429")
    # print(response.status_code)
    # print()
    # print(response.content)

    
    x = Post.objects.filter(status=Post.ACTIVE)
    
    trending = []
    # x = Post.objects.all().order_by('-date_created').values()
    
    
    # added all the blog posts from the DB to a list
    editor_posts = []
    top_posts = []
    for post in x:
        # ch = random.choice(post)
        editor_posts.append(post)
        top_posts.append(post)
        trending.append(post)

        random_posts = editor_posts[::2]
        topPosts = top_posts[::3]


    num = random.randint(1,9)
    print(num)
    trending = trending[::4]

    print(trending)
        
        
    # this line of code is to display the categories from  the DB to the website   
    categories = Category.objects.all()


    context = {'posts': topPosts, 'rand_posts': random_posts, "trending_post": trending, "categories": categories, "site": site}
    return render(request, 'blog/home.html', context)


# view function for blog posts
def blog_post(request, category_slug, slug):
    
    
     # Your API key, available from your account page
    API_KEY = config("GEOLOCATOR_API_KEY")

    # URL to send the request to
    request_url = 'https://ipgeolocation.abstractapi.com/v1/?api_key=' + API_KEY
    # response = requests.get(request_url)
    # result = json.loads(response.content)
    # # print(result)
    # print("")
    # print('ip_address: {}'.format(result['ip_address']))
    # print('City: {}'.format(result['city']))
    # print('Country: {}'.format(result['country']))
    
    post  = get_object_or_404(Post, slug=slug, status=Post.ACTIVE)
    
    recent_posts = []
    previous_posts = []
    
    datas = Post.objects.all()
    
    for data in datas:
        recent_posts.append(data)
        previous_posts.append(data)
        
    recent_posts = recent_posts[:-2]
    previous_posts = previous_posts[3:]
    print(data)
    
    categories = Category.objects.all()
    
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
        

    context = {'post': post, "recent_posts": recent_posts, "previous_posts": previous_posts, "form": form, "categories": categories, "site": site}
    return render(request, 'blog/blog-post.html', context)


# view function for categories
def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    
    posts = category.posts.filter(status=Post.ACTIVE)
    
    categories = Category.objects.all()
    
    return render(request, "blog/category.html", {'category': category, 'posts': posts, "categories": categories, "site": site})



# view function for search
def search(request):
    query = request.GET.get('query', '')
    
    posts = Post.objects.filter(status=Post.ACTIVE).filter(Q(title__icontains=query) | Q(intro__icontains=query) | Q(body__icontains=query))
    
    categories = Category.objects.all()
    
    return render(request, 'blog/search.html', {"posts": posts, "query": query, "categories": categories, "site": site})



# view function for contact
def contact(request):

    if request.method == "POST":
        name = request.POST["name"]
        subject = request.POST["subject"]
        from_email = request.POST["email"]
        phone = request.POST["phone"]
        payload = request.POST["message"]

        mail = ReceivedMail.objects.create(name=name, subject=subject, email=from_email, phone=phone, message=message)
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

    categories = Category.objects.all()
    context = {"categories": categories, "site": site}
    return render(request, 'blog/contact.html', context)


# view function for robot_txt
def robot_txt(request):
    text = [
        "User-Agent: *",
        "Disallow: /admin/",
    ]
    return HttpResponse("\n".join(text), content_type="text/plain")


