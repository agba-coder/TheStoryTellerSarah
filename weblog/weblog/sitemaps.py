from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse


from blog.models import Post, Category

class CategorySitemap(Sitemap):
    """docstring for CategorySitemap"""
    def items(self):
        return Category.objects.all()


class PostSitemap(Sitemap):
    def items(self):
        return Post.objects.filter(status=Post.ACTIVE)
    
    def lastmod(self, obj):
        return obj.date_created