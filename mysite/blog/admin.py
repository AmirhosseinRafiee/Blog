from django.contrib import admin
from blog.models import Post, Category, Comment
from django_summernote.admin import SummernoteModelAdmin

# @admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
  date_hierarchy = 'created_date'
  empty_value_display = '-empty-'
  # fields = ('title', 'content', 'status', 'published_date') 
  exclude = ('counted_view',)
  list_display = ('title', 'author', 'status', 'login_require', 'counted_view', 'created_date', 'published_date')
  # ordeing = '-created_date'
  list_filter = ('status', 'author')
  search_fields = ('title', 'content')
  summernote_fields = ('content',)

class CommentAdmin(admin.ModelAdmin):
  date_hierarchy = 'created_date'
  empty_value_display = '-empty-'
  list_display = ('name', 'subject', 'approved', 'created_date')
  list_filter = ('approved', 'post')
  search_fields = ('name', 'subject')

admin.site.register(Comment, CommentAdmin)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
