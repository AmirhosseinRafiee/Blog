from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from taggit.managers import TaggableManager
from accounts.models import Profile

class Category(models.Model):
  name = models.CharField(max_length=255)

  class Meta:
    verbose_name_plural = 'Categories'

  def __str__(self):
    return self.name

class Post(models.Model):
  author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
  image = models.ImageField(upload_to='blog/', default='default.jpg')
  title = models.CharField(max_length=255)
  content = models.TextField()
  category = models.ManyToManyField(Category)
  tags = TaggableManager(blank=True)
  counted_view = models.PositiveIntegerField(default=0)
  status = models.BooleanField(default=False)
  login_require = models.BooleanField(default=False)
  published_date = models.DateTimeField(default=now ,null=True)
  created_date = models.DateTimeField(auto_now_add=True)
  updated_date = models.DateTimeField(auto_now=True)
  class Meta:
    ordering = ['-created_date']
    # verbose_name = 'پست'
    # verbose_name_plural = 'پست ها'
  
  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse('blog:single', kwargs={'pk': self.id})
  
  def get_absolute_api_url(self):
    return reverse('blog:api-v1:post-detail', kwargs={'pk': self.id})
  
  def get_snippet(self):
    return self.content[:40]


class Comment(models.Model):
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  name = models.CharField(max_length=255)
  email = models.EmailField()
  subject = models.CharField(max_length=255)
  message = models.TextField()
  approved = models.BooleanField(default=False)
  created_date = models.DateTimeField(auto_now_add=True)
  published_date = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ['-created_date']