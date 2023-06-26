from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PeopleWhoVistedYourSite(models.Model):
    ip_address = models.GenericIPAddressField(editable=True, unique=True)
    # city = models.CharField(editable=False)
    # country = models.CharField(editable=False)
    date_visted = models.DateTimeField(auto_now_add=True)
    
    # def __str__(models.Model):
    #     return f"{self.city}, {self.country}"
    
    # class Meta:
    #     ordering = ("-date_visited",)


class Tag(models.Model):
    hash_tag = models.CharField(max_length=100)
    
    def __str__(self):
        return f"#{self.hash_tag}"

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    
    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return self.title 

    def get_absolute_url(self):
        return "/%s/" % self.slug


class Post(models.Model):
    
    ''' 
    the ACTIVE & DRAFT functionalities is to determine if a 
    blog post should or is posted or drafted
    
    '''
    
    ACTIVE = "posted"
    DRAFT = "draft"
    # TRENDING = "posted & added to trending"
    
    # label that will show in the admin site
    
    CHOICES_STATUS = (
        (ACTIVE, "Posted"),
        (DRAFT, "Add to Draft"),
        # (TRENDING, "Posted & Add to Trending"),
    )
    
    
    category = models.ForeignKey(Category, related_name="posts", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    intro = models.TextField()
    body = models.TextField()
    image = models.ImageField(default="default.jpg", upload_to="post_images/")
    read_duration_in_minutes = models.IntegerField()
    hash_tag = models.ForeignKey(Tag, related_name="post_tag", on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, editable=True)
    status = models.CharField(max_length=26, choices=CHOICES_STATUS, default=ACTIVE)
    
    
    def __str__(self):
        return self.title
    
    # to sort blog post by date created
    class Meta:
        ordering = ('-date_created',)
    
    def get_absolute_url(self):
        return '/%s/%s/' % (self.category. slug,self.slug)
        
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} commented '{self.body}' in {self.post}\n"


class Newsletter(models.Model):
    subscribed_email_address = models.EmailField(unique=True)
    date_subscribed = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.subscribed_email_address}"
    
    class Meta:
        ordering = ("-date_subscribed",)


class ReceivedMail(models.Model):
    name = models.CharField(max_length=50, editable=False)
    subject = models.CharField(max_length=100, editable=False)
    email = models.EmailField(editable=False)
    phone = models.CharField(max_length=16, editable=False)
    message = models.TextField(editable=False)
    date_received = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"A message from {self.email}"
    
    class Meta:
        ordering = ("-date_received",)
        verbose_name_plural = 'Categories'
