from django.urls import path
from blog import views
from blog.feeds import LatestEntriesFeed

app_name = 'blog'

urlpatterns = [
    path('', views.blog, name='index'),
    path('<int:pid>', views.blog_single, name='single'),
    path('category/<str:cat_name>', views.blog, name='category'),
    path('tag/<str:tag_name>', views.blog, name='tag'),
    path('author/<str:author_username>', views.blog, name='author'),
    path('search', views.blog_search, name='search'),  
    path('rss/feed/', LatestEntriesFeed()),
]