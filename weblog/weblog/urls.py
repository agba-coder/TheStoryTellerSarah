"""weblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.contrib import sitemaps
from django.contrib.sitemaps.views import sitemap 

from django.conf import settings
from django.conf.urls.static import static

from authentication import views as user_views

from django.contrib.auth import views as auth_views


from .sitemaps import PostSitemap, CategorySitemap

sitemaps = {'post': PostSitemap, "categories": CategorySitemap}

handler400 = "blog.views.handler400"
handler403 = "blog.views.handler403"
handler404 = "blog.views.handler404"
handler500 = "blog.views.handler500"


urlpatterns = [
    # path('favicon.ico', lambda _ : redirect('static/images/favicon.ico', permanent=True)),
    path("sitemaps.xml", sitemap, {"sitemaps": sitemaps}),
    path('admin/', admin.site.urls),
    
    path('accounts/auth/password-reset/verify', 
        auth_views.PasswordResetView.as_view(
            template_name='authentication/password_reset.html',
            html_email_template_name='emails/index.html'
        ),
        name='password_reset'
    ),
    
    path('accounts/auth/password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='authentication/password_reset_done.html'),
         name='password_reset_done'),
    
    path('accounts/auth/password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='authentication/password_reset_confirm.html'),
         name='password_reset_confirm'),
    
    path('accounts/auth/password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'),
         name='password_reset_complete'),
    
    path('', include('blog.urls')),
    path('accounts/auth/', include('authentication.urls')),
    path('favicon.ico', lambda _ : redirect('static/images/favicon.ico', permanent=True)),
    
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)