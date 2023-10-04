from django.forms import DateTimeInput
from django_filters import FilterSet, DateTimeFilter
from .models import Post


class PostFilter(FilterSet):
    added_after = DateTimeFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%d.%m.%Y',
            attrs={'type': 'date'},  # вместо datetime-local используется date, т.к. время создания статьи не важно
        ),
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'postCategory': ['exact'],
        }
