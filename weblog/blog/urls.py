from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path("robot.txt", views.robot_txt, name="robot_txt"),
    path('contact-me', views.contact, name='contact'),
    path('<slug:category_slug>/<slug:slug>/', views.blog_post, name="blog_post"),
    path('<slug:slug>/', views.category, name="category_detail"),
    path('favicon.ico', lambda _ : redirect('static/images/favicon.ico', permanent=True)),
    
]

# ?search=black