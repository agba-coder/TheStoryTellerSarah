from django.contrib import admin

from .models import Post, Comment, Category, Tag, PeopleWhoVistedYourSite

# Register your models here.

# Added the Tag functionalies for the admin site
class TagAdmin(admin.ModelAdmin):
    search_fields = ["hash_tag"]
    list_display = ["hash_tag"]

# Integrated the Admin Category for search filter and sort functionalites
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':("title",)}
    search_fields = ["title"]
    list_display = ["title"]

# Integrated the Admin search for Post search filter and sort functionalities
class PostAdmin(admin.ModelAdmin):
    search_fields = ["title", "intro", "body"]
    list_display = ["title", "slug", "date_created", "status"]
    list_filter = ["date_created", "status"]
    prepopulated_fields = {'slug':("title",)}
    

#Integrated the Admin comment, comment filter and sort-comment functionalities   
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "body", "post", "date_created"]
    
# registered Category Model to the admin site
admin.site.register(Category, CategoryAdmin)


# registered Post Model to the admin site
admin.site.register(Post, PostAdmin)

# registered Comment Model to the admin site
admin.site.register(Comment, CommentAdmin)

# registered Tag Model to the admin site
admin.site.register(Tag, TagAdmin)
admin.site.register(PeopleWhoVistedYourSite)