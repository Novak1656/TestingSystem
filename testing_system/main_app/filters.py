import django_filters
from .models import Test, Tag, Category
from users_app.models import User


class TestsFilter(django_filters.FilterSet):
    ORDERING_LIST = [
        ('published_at', 'Сначала новые'),
        ('-published_at', 'Сначала старые'),
        ('-passed_times', 'Больше всего прошли'),
        ('passed_times', 'Меньше всего прошли'),
        ('title', 'По названию по возрастанию'),
        ('-title', 'По названию по убыванию'),
    ]

    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    author = django_filters.ModelChoiceFilter(field_name='author', queryset=User.objects.all())
    category = django_filters.ModelChoiceFilter(field_name='category', queryset=Category.objects.all())
    tags = django_filters.ModelMultipleChoiceFilter(field_name='tags', queryset=Tag.objects.all())
    ordering = django_filters.OrderingFilter(choices=ORDERING_LIST, field_name='ordering')

    class Meta:
        model = Test
        fields = {'title', 'author', 'category', 'tags'}
