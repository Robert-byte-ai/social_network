from django_filters.rest_framework import FilterSet, filters

from .models import Post


class PostFilter(FilterSet):
    follow = filters.BooleanFilter(method='filter_follow')
    read = filters.BooleanFilter(method='filter_read')

    def filter_follow(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(author__following__user=user)
        return queryset

    def filter_read(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(read_posts__user=user)
        return queryset

    class Meta:
        model = Post
        fields = ('follow', 'read')
