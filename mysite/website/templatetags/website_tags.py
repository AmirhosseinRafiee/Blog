from django.utils import timezone
from django import template
from blog.models import Post

register = template.Library()


@register.inclusion_tag("website/latest-blog.html", takes_context=True)
def latest_post(context):
    request = context["request"]
    posts = Post.objects.filter(
        status=True, published_date__lte=timezone.now()
    ).order_by("-published_date")
    if not request.user.is_authenticated:
        posts = posts.filter(login_require=False)
    posts = posts[:6]
    return {"posts": posts}
