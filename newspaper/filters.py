from django_filters import FilterSet
from .models import Post

class PostFilter(FilterSet):
    class Meta:
        model = Post
        # fields = ('author__user__username', 'date')

        fields = {
            'author__user__username': ['icontains'],
            'date': ['gt'],
            'title_post': ['icontains']
        }