from django import template
from blog.models import Category, Post, Comment

register = template.Library()

@register.simple_tag(name='totalposts')
def function():
  posts = Post.objects.filter(status=1)
  return posts

@register.simple_tag(name='comments_count')
def function(pid):
  return Comment.objects.filter(post=pid,approved=True).count()

@register.filter
def snippet(value,arg=20):
  return value[:arg] + "..."

@register.inclusion_tag('blog/blog-popular-posts.html')
def popularposts(arg=4):
  posts = Post.objects.filter(status=1).order_by('-counted_view')[:arg]
  return {'posts': posts}

@register.inclusion_tag('blog/blog-post-categories.html')
def postcategories():
  posts = Post.objects.filter(status=1)
  categories = Category.objects.all()
  cat_dict = {}
  for cat in categories:
    cat_dict[cat] = posts.filter(category=cat).count()
  return {'categories': cat_dict}

