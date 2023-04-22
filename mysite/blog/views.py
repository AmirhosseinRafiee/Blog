from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from blog.forms import CommentForm
from blog.models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

def blog(request, **kwargs):
    posts = Post.objects.filter(status=1, published_date__lte=timezone.now())
    if kwargs.get('cat_name') != None:
        posts = posts.filter(category__name=kwargs['cat_name'])
    if kwargs.get('author_username') != None:
        posts = posts.filter(author__username=kwargs['author_username'])
    if kwargs.get('tag_name') != None:
        posts = posts.filter(tags__name__in=[kwargs['tag_name']])
    paginator = Paginator(posts, 4)
    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(1)
    context = {'posts': posts}
    return render(request, 'blog/blog-home.html', context)

def blog_single(request, pid):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'your comment submited successfully.')
        else:
            messages.error(request, "your comment didn't submited.")
    posts = Post.objects.filter(status=1, published_date__lte=timezone.now())
    post = get_object_or_404(posts, pk=pid)
    if not post.login_require or request.user.is_authenticated:
        post.counted_view += 1
        post.save()
        comments = Comment.objects.filter(post=post.id, approved=True)
        try:
            next_post = posts.filter(id__gt=post.id).order_by("id")[0:1].get()
        except Post.DoesNotExist:
            # Post.objects.aggregate(Min("id"))['id__min']
            next_post = None
        try:
            prev_post = posts.filter(id__lt=post.id).order_by("-id")[0:1].get()
        except Post.DoesNotExist:
            # Post.objects.aggregate(Max("id"))['id__max']
            prev_post = None
        context = {'post': post, 'prev_post': prev_post, 'next_post': next_post, 'comments': comments}
        return render(request, 'blog/blog-single.html', context)
    else: # post is login required and user isn't authenticated 
        return redirect(reverse('accounts:login')+f'?next=/blog/{post.id}')


def blog_category(request, cat_name):
    posts = Post.objects.filter(status=1).filter(category__name=cat_name)
    context = {'posts': posts}
    return render(request, 'blog/blog-home.html', context)

def blog_search(request):
    posts = Post.objects.filter(status=1, published_date__lte=timezone.now())
    if s:= request.GET.get('s'):
        posts = posts.filter(content__contains=s)
    context = {'posts': posts}
    return render(request, 'blog/blog-home.html', context)
