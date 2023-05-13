from django.urls import path, include
from blog import views
from blog.feeds import LatestEntriesFeed

app_name = "blog"

urlpatterns = [
    path("", views.BlogView.as_view(), name="index"),
    path("<int:pid>/", views.BlogSingleView.as_view(), name="single"),
    path("comment/<int:pid>/", views.CommentView.as_view(), name="comment"),
    path("category/<str:cat_name>/", views.BlogView.as_view(), name="category"),
    path("tag/<str:tag_name>/", views.BlogView.as_view(), name="tag"),
    path("author/<int:author_profile_id>/", views.BlogView.as_view(), name="author"),
    # path('search/', views.blog_search, name='search'),
    path("api/v1/", include("blog.api.v1.urls")),
    path("rss/feed/", LatestEntriesFeed()),
]
