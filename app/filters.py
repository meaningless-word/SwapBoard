from django.forms import DateInput
from django_filters import FilterSet, CharFilter, ModelMultipleChoiceFilter, DateTimeFilter, TypedMultipleChoiceFilter
from .models import Post


class PostFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='по вхождению',
    )
    cType = TypedMultipleChoiceFilter(
        field_name='categoryType',
        choices=Post.CATEGORY_CHOICES,
        label='тип',
    )
    dateCreation = DateTimeFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        widget=DateInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
        label='не ранее',
    )
