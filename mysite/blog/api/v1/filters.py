from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from taggit.managers import TaggableManager
from taggit.models import Tag
from ...models import Post, Category


class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass
    
def categories(request):
    return Category.objects.all()

def tags(request):
    return Tag.objects.all()

class PostFilter(filters.FilterSet):
    # category = filters.CharFilter(field_name='category__name', lookup_expr='iexact')
    # category_in = filters.CharFilter(method='filter_category', label='Category is in', help_text='Multiple values may be separated by commas.')
    category_in = CharInFilter(field_name='category__name', lookup_expr='in', distinct=True)
    tag = filters.CharFilter(field_name='tags__name', lookup_expr='iexact', label='tag')    
    tags_in = CharInFilter(field_name='tags__name', lookup_expr='in', distinct=True)
    # tags_in = filters.CharFilter(method='filter_tags', label='tags')
    published_date = filters.DateFromToRangeFilter(field_name='published_date')
    category = filters.ModelChoiceFilter(lookup_expr='icontains', field_name='category__name' , to_field_name='name', queryset=categories)
    category__in = filters.ModelMultipleChoiceFilter(lookup_expr='icontains', field_name='category__name' , to_field_name='name', queryset=categories)
    tags__in = filters.ModelMultipleChoiceFilter(lookup_expr='icontains', field_name='tags__name', to_field_name='name', queryset=tags)

    class Meta:
        model = Post
        fields = {
            'author': ['exact'],
        }
        filter_overrides = {
            TaggableManager: {
                'filter_class': filters.CharFilter,
            },
        }

    def filter_category(self, queryset, name, value):
        categories = value.split(',')
        return queryset.filter(category__name__in=categories).distinct()
    
    def filter_tags(self, queryset, name, value):
        # query = Q()
        # for tag in value.split(','):
        #     query |= Q(tags__name__contains=tag)
        # return queryset.filter(query)
        tags = value.split(',')
        return queryset.filter(tags__name__in=tags).distinct()


class PostCustomOrderFilter(OrderingFilter):

    def filter_queryset(self, request, queryset, view):
        order_fields = []
        ordering = self.get_ordering(request, queryset, view)
        if ordering:
            for field in ordering:
                symbol = "-" if "-" in field else ""
                order_fields.append(symbol+field.lstrip('-'))
        if 'counted_view' in order_fields:
            order_fields.remove('counted_view')
        if order_fields:
            return queryset.order_by(*order_fields)

        return queryset
    
    def get_template_context(self, request, queryset, view):
        current = self.get_ordering(request, queryset, view)
        current = None if not current else current[0]
        options = []
        context = {
            'request': request,
            'current': current,
            'param': self.ordering_param,
        }
        for key, label in self.get_valid_fields(queryset, view, context):
            if key != 'counted_view':
                options.append((key, '%s - %s' % (label, _('ascending'))))        
            options.append(('-' + key, '%s - %s' % (label, _('descending'))))
        # options.remove(('counted_view', 'counted_view - ascending'))
        context['options'] = options
        return context