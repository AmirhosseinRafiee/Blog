from django import template
from blog.models import Post
register = template.Library()

@register.inclusion_tag('website/latest-blog.html')
def latestpost():
  posts = Post.objects.filter(status=1).order_by('-published_date')[0:6]
  return {'posts': posts}