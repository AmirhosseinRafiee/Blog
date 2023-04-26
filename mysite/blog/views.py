# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from django.utils import timezone
from django.http import Http404
from django.core.paginator import InvalidPage
from .forms import CommentForm
from .models import Post, Comment


# def blog(request, **kwargs):
#     posts = Post.objects.filter(status=1, published_date__lte=timezone.now())
#     if kwargs.get('cat_name') != None:
#         posts = posts.filter(category__name=kwargs['cat_name'])
#     if kwargs.get('author_profile_id') != None:
#         posts = posts.filter(author=kwargs['author_profile_id'])
#     if kwargs.get('tag_name') != None:
#         posts = posts.filter(tags__name__in=[kwargs['tag_name']])
#     paginator = Paginator(posts, 4)
#     page_number = request.GET.get('page')
#     try:
#         posts = paginator.page(page_number)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(1)
#     context = {'posts': posts}
#     return render(request, 'blog/blog-home.html', context)

class BlogView(ListView):
    template_name = 'blog/blog-home.html'
    context_object_name = 'posts'
    http_method_names = ['get']
    paginate_by = 2

    def get_queryset(self):
        posts = Post.objects.filter(status=True, published_date__lte=timezone.now())
        if not self.request.user.is_authenticated:
            posts = posts.filter(login_require=False)
        if (cat_name := self.kwargs.get('cat_name')) != None:
            posts = posts.filter(category__name=cat_name)
        if (author_profile_id := self.kwargs.get('author_profile_id')) != None:
            posts = posts.filter(author=author_profile_id)
        if (tag_name := self.kwargs.get('tag_name')) != None:
            posts = posts.filter(tags__name__in=[tag_name])
        if search := self.request.GET.get('s'):
            posts = posts.filter(Q(title__icontains=search) | Q(content__icontains=search))
        return posts

    def paginate_queryset(self, queryset, page_size):
        """
        This is an exact copy of the original method, jut changing `page` to `get_page` method to prevent errors with out of range pages.
        """
        paginator = self.get_paginator(
            queryset, page_size, orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty())
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404(_('Page is not “last”, nor can it be converted to an int.'))
        try:
            page = paginator.get_page(page_number)
            return (paginator, page, page.object_list, page.has_other_pages())
        except InvalidPage as e:
            raise Http404(_('Invalid page (%(page_number)s): %(message)s') % {
                'page_number': page_number,
                'message': str(e)
            })


# def blog_single(request, pid):
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'your comment submitted successfully.')
#         else:
#             messages.error(request, "your comment didn't submitted.")
#     posts = Post.objects.filter(status=1, published_date__lte=timezone.now())
#     post = get_object_or_404(posts, pk=pid)
#     if not post.login_require or request.user.is_authenticated:
#         post.counted_view += 1
#         post.save()
#         comments = Comment.objects.filter(post=post.id, approved=True)
#         try:
#             next_post = posts.filter(id__gt=post.id).order_by("id")[0:1].get()
#         except Post.DoesNotExist:
#             # Post.objects.aggregate(Min("id"))['id__min']
#             next_post = None
#         try:
#             prev_post = posts.filter(id__lt=post.id).order_by("-id")[0:1].get()
#         except Post.DoesNotExist:
#             # Post.objects.aggregate(Max("id"))['id__max']
#             prev_post = None
#         context = {'post': post, 'prev_post': prev_post, 'next_post': next_post, 'comments': comments}
#         return render(request, 'blog/blog-single.html', context)
#     else: # post is login required and user isn't authenticated 
#         return redirect(reverse('accounts:login')+f'?next=/blog/{post.id}')
    

class BlogSingleView(DetailView):
    template_name = 'blog/blog-single.html'
    pk_url_kwarg = 'pid'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        post_obj = self.get_object()
        if post_obj.login_require and not self.request.user.is_authenticated:
            return redirect('{}?next={}'.format(reverse('accounts:login') ,self.request.path))
        post_obj.counted_view += 1
        post_obj.save()
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        posts = Post.objects.filter(status=True, published_date__lte=timezone.now())
        # if not self.request.user.is_authenticated:
        #     posts = posts.filter(login_require=False)
        if (cat_name := self.kwargs.get('cat_name')) != None:
            posts = posts.filter(category__name=cat_name)
        if (author_profile_id := self.kwargs.get('author_profile_id')) != None:
            posts = posts.filter(author=author_profile_id)
        if (tag_name := self.kwargs.get('tag_name')) != None:
            posts = posts.filter(tags__name__in=[tag_name])
        self.queryset = posts
        return posts
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = self.queryset
        post = context['post']
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
        context['prev_post'] = prev_post
        context['next_post'] = next_post
        context['comments'] = comments
        return context

    
class CommentView(SuccessMessageMixin ,CreateView):
    form_class = CommentForm
    http_method_names = ['post']
    success_message = 'your comment submitted successfully.'

    def get_success_url(self):    
        if last_page := self.request.GET.get('lastPage'):
            url = last_page
        else:
            url = '/blog/'
        return url
    
    def form_invalid(self, form):
        messages.error(self.request, "your comment didn't submitted.")       
        if last_page := self.request.GET.get('lastPage'):
            url = last_page
        else:
            url = '/blog/'
        return redirect(url)
    
    def dispatch(self, request, *args, **kwargs):
        posts = Post.objects.filter(status=True, published_date__lte=timezone.now())
        post = get_object_or_404(posts, pk=kwargs['pid'])
        if post.login_require and not request.user.is_authenticated:
            messages.error(request, "permission denied")
            return redirect('/blog/')
        return super().dispatch(request, *args, **kwargs)


# def blog_category(request, cat_name):
#     posts = Post.objects.filter(status=1).filter(category__name=cat_name)
#     context = {'posts': posts}
#     return render(request, 'blog/blog-home.html', context)

# class BlogCategory(ListView):
#     template_name = 'blog/blog-category.html'

#     def get_queryset(self):
#         queryset = Post.objects.filter(status=1).filter(category__name=self.kwargs['cat_name'])
#         return queryset

# def blog_search(request):
#     posts = Post.objects.filter(status=1, published_date__lte=timezone.now())
#     if s:= request.GET.get('s'):
#         posts = posts.filter(content__contains=s)
#     context = {'posts': posts}
#     return render(request, 'blog/blog-home.html', context)


