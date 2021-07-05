from django.db.models import Max
from django.utils import timezone
from django_filters import rest_framework as fltr

from .models import Post


class PostFilter(fltr.FilterSet):
    status = fltr.ChoiceFilter(field_name='status', method='filter_status', choices=Post.STATUS_CHOICES)
    author = fltr.CharFilter(method='filter_author')
    title = fltr.CharFilter(method='filter_title')
    activity = fltr.CharFilter(method='filter_max')

    def filter_max(self, queryset, name, value):

        if value == 'max':
            maximun = queryset.aggregate(Max('activity_count'))
            if maximun['activity_count__max'] is not None:
                return queryset.filter(activity_count__gte=maximun['activity_count__max'])
            else:
                return queryset

    def filter_status(self, queryset, name, value):
        if value == Post.ACTIVE:
            return queryset.filter(expiry_date__gt=timezone.now())
        if value == Post.EXPIRED:
            return queryset.filter(expiry_date__lt=timezone.now())

    def filter_author(self, queryset, name, value):
        return queryset.filter(user__username=value)

    def filter_title(self, queryset, name, value):
        return queryset.filter(title__icontains=value)

    class Meta:
        model = Post
        fields = ['status', 'topic', 'timestamp', 'author', 'title', 'activity']
