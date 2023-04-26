from django.contrib import admin
from blog.models import Post, Category, Comment
from django_summernote.admin import SummernoteModelAdmin
from accounts.models import Profile


class PostAdmin(SummernoteModelAdmin):
  date_hierarchy = 'created_date'
  empty_value_display = '-empty-'
  # fields = ('title', 'content', 'status', 'published_date') 
  # exclude = ('counted_view',)
  list_display = ('title', 'author', 'status', 'login_require', 'counted_view', 'created_date', 'published_date')
  readonly_fields = ('counted_view',)
  # ordeing = '-created_date'
  list_filter = ('status', 'author')
  search_fields = ('title', 'content')
  summernote_fields = ('content',)
  
  def formfield_for_foreignkey(self, db_field, request, **kwargs):
    if db_field.name == 'author':
        # setting the user from the request object
        kwargs['initial'] = Profile.objects.get(user=request.user)
        # making the field readonly
        kwargs['disabled'] = True
    return super().formfield_for_foreignkey(db_field, request, **kwargs)

  def save_model(self, request, obj, form, change):
    # profile = Profile.objects.get(user=request.user)
    # obj.author = profile
    super().save_model(request, obj, form, change)


class CommentAdmin(admin.ModelAdmin):
  date_hierarchy = 'created_date'
  empty_value_display = '-empty-'
  list_display = ('name', 'subject', 'approved', 'created_date')
  list_filter = ('approved', 'post')
  search_fields = ('name', 'subject')

admin.site.register(Comment, CommentAdmin)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
