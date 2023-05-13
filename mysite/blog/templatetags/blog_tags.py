from django import template
from django.utils import timezone
from blog.models import Category, Post, Comment

register = template.Library()


@register.simple_tag(name="totalposts", takes_context=True)
def function(context):
    request = context["request"]
    posts = Post.objects.filter(status=True, published_date__lte=timezone.now())
    if not request.user.is_authenticated:
        posts = posts.filter(login_require=False)
    return posts


@register.simple_tag(name="comments_count")
def function2(pid):
    return Comment.objects.filter(post=pid, approved=True).count()


@register.filter
def snippet(value, arg=20):
    return value[:arg] + "..."


@register.inclusion_tag("blog/blog-popular-posts.html", takes_context=True)
def popular_posts(context, arg=4):
    request = context["request"]
    posts = Post.objects.filter(
        status=True, published_date__lte=timezone.now()
    ).order_by("-counted_view")
    if not request.user.is_authenticated:
        posts = posts.filter(login_require=False)
    posts = posts[:arg]
    return {"posts": posts}


@register.inclusion_tag("blog/blog-post-categories.html")
def post_categories():
    posts = Post.objects.filter(status=1)
    categories = Category.objects.all()
    cat_dict = {}
    for cat in categories:
        cat_dict[cat] = posts.filter(category=cat).count()
    return {"categories": cat_dict}
